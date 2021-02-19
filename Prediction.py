import numpy as np
import re


class Prediction:
    def __init__(self, model, vocab):
        if not isinstance(vocab, dict):
            raise TypeError('Only "dict" type can be used as vocabulary')
        self.model = model
        self.vocab = vocab
        self.smiles = ""
        self.max_reg = 130
        self.max_prod = 80
        self.smiles_tokenizer = re.compile(
            r'(\[[^\]]+]|Br?|Cl?|N|O|S|P|F|I|b|c|n|o|s|se?|p|\(|\)|\.|=|#|'
            r'-|\+|\\\\|\/|:|~|@|\?|>|\*|\$|\%[0-9]{2}|[0-9])'
        )
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
        self.data = list()

    def get_data(self):
        reg_batch = np.zeros((1, self.max_reg))
        prod_batch = np.zeros((1, self.max_prod))
        reg_batch[:, 0] = self.vocab['SOS']
        prod_batch[:, 0] = self.vocab['SOS']
        tokens_prod = list()
        if ">>" in self.smiles:
            reg = str(self.smiles.split('>>')[0])
            prod = str(self.smiles.split('>>')[1])
            tokens_prod = [token for token in self.smiles_tokenizer.split(prod) if token]
        else:
            reg = str(self.smiles)
        tokens_reg = [token for token in self.smiles_tokenizer.split(reg) if token]
        if len(tokens_reg) > self.max_reg - 2 or len(tokens_prod) > self.max_prod - 2:
            raise ValueError("Not in reg / prod max lengths!")
        for i in range(len(tokens_reg)):
            reg_batch[0][i + 1] = self.vocab[tokens_reg[i]]
        for i in range(len(tokens_prod)):
            prod_batch[0][i + 1] = self.vocab[tokens_prod[i]]
        self.data = [reg_batch, prod_batch]
        return [self.data[0][:], self.data[1][:, :-1], self.data[1][:, 1:]], self.data[1][:, 1:]

    def beam_pred(self, data, k):
        inputs, out = data
        enc_inp, tar_inp, tar_out = inputs
        bt, seq = tar_out.shape

        vocab_size = len(self.inv_vocab)
        sos_token = [ind for ind, t in self.inv_vocab.items() if t == 'SOS'][0]

        def get_sos(bt, seq):
            z = np.zeros((bt, seq), dtype=np.int)
            z[:, 0] = sos_token
            return z

        sos = get_sos(bt, seq)
        inp_list = [get_sos(bt, seq) for i in range(k)]
        probs = []
        endb = [0 for i in range(bt)]
        final_beams = [[] for i in range(bt)]

        for step in range(seq):
            temp_inp = [get_sos(bt, seq) for i in range(k)]
            if step == 0:
                prediction = self.model.predict([enc_inp, sos, tar_out])

                best_ind = prediction[:, step, :].argsort()[:, -k:][:, ::-1]
                probs = np.take_along_axis(prediction[:, step, :], best_ind, axis=-1)

                real_ind = best_ind
                beam_ind = best_ind // vocab_size

            else:
                out_list = []
                for beam in range(k):
                    prediction = self.model.predict([enc_inp, inp_list[beam], tar_out])
                    p = prediction[:, step, :] * probs[:, beam:beam + 1]

                    for rxn in range(bt):
                        if beam >= k - endb[rxn]:
                            p[rxn, :] *= 0

                    out_list.append(p)

                outs = np.concatenate(out_list, axis=-1)

                best_ind = outs.argsort()[:, -k:][:, ::-1]
                probs = np.take_along_axis(outs, best_ind, axis=-1)
                real_ind = best_ind % vocab_size
                beam_ind = best_ind // vocab_size

            for rxn in range(bt):
                if step == seq - 1:
                    c = 0
                    while c < k - endb[rxn]:
                        from_beam = beam_ind[rxn, c]
                        new_seq = np.concatenate([inp_list[from_beam][rxn, 1:],
                                                  real_ind[rxn, c:c + 1]], axis=-1)
                        final_beams[rxn].append(list(new_seq))

                        c += 1
                else:
                    c = 0
                    padc = 0
                    while c < k - endb[rxn]:
                        from_beam = beam_ind[rxn, c]
                        pad = seq - step - 2
                        new_seq = np.concatenate([inp_list[from_beam][rxn, :step + 1],
                                                  real_ind[rxn, c:c + 1],
                                                  np.zeros(pad).astype(np.int)], axis=-1)
                        if real_ind[rxn, c] == 0:
                            padc += 1
                            final_beams[rxn].append(list(new_seq[1:]))
                        else:
                            temp_inp[c - padc][rxn] = new_seq
                        c += 1

                    endb[rxn] += padc

            inp_list = temp_inp

        return final_beams

    def prediction(self, smiles):
        if not isinstance(smiles, str):
            raise TypeError('Only "str" type can be used as SMILES')
        self.smiles = smiles
        matrix = self.get_data()
        pred_list = self.beam_pred(matrix, 1)
        true_smiles = ''.join([self.inv_vocab[i] for i in matrix[1][0]]).split('pad')[0]
        pred_smiles = []
        for rxn in pred_list:
            pred_smi = ''.join([self.inv_vocab[i] for i in rxn])

            if 'pad' in pred_smi and len(pred_smi.split('pad')[0]) > 0:
                pred_smi = pred_smi.split('pad')[0]
                pred_smiles.append(pred_smi)
            else:
                continue

        if str(true_smiles) in pred_smiles:
            return true_smiles
        else:
            return pred_smiles[0]
