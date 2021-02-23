import numpy as np
import re

class Prediction:
    def __init__(self, smiles, vocab):
        if not isinstance(smiles, str):
            raise TypeError('Only "str" type can be used as SMILES')
        if not isinstance(vocab, dict):
            raise TypeError('Only "dict" type can be used as vocabulary')
        self.smiles = smiles
        self.vocab = vocab
        self.max_reg = 130
        self.max_prod = 80
        self.smiles_tokenizer = re.compile(
            r'(\[[^\]]+]|Br?|Cl?|N|O|S|P|F|I|b|c|n|o|s|se?|p|\(|\)|\.|=|#|'
            r'-|\+|\\\\|\/|:|~|@|\?|>|\*|\$|\%[0-9]{2}|[0-9])'
        )
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
        self.data = list()

    def get_matrix(self):
        reg_batch = np.zeros((1, self.max_reg))
        prod_batch = np.zeros((1, self.max_prod))
        reg_batch[:, 0] = self.vocab['SOS']
        prod_batch[:, 0] = self.vocab['SOS']
        if ">>" in self.smiles:
            reg = str(self.smiles.split('>>')[0])
            prod = str(self.smiles.split('>>')[1])
            tokens_prod = [token for token in self.smiles_tokenizer.split(prod) if token]
        else:
            reg = str(self.smiles)
        tokens_reg = [token for token in self.smiles_tokenizer.split(reg) if token]
        if len(tokens_prod) > self.max_prod - 2 or len(tokens_reg) > self.max_reg - 2:
            raise ValueError("Not in reg / prod max lengths!")
        for i in range(len(tokens_reg)):
            reg_batch[0][i + 1] = self.vocab[tokens_reg[i]]
        for i in range(len(tokens_prod)):
            prod_batch[0][i + 1] = self.vocab[tokens_prod[i]]
        self.data = [reg_batch, prod_batch]
        return [self.data[0][:], self.data[1][:, :-1], self.data[1][:, 1:]], self.data[1][:, 1:]

        def get_data(self):
            yield [self.data[0][:], self.data[1][:, :-1], self.data[1][:, 1:]], self.data[1][:, 1:]


vocabulary = {'O': 1, '(': 2, 'C': 3, ')': 4, 'N': 5, '.': 6, '[Cl-]': 7, 'c': 8, '1': 9, 'n': 10, '2': 11, '3': 12, '=': 13, '>': 14, '[Li]': 15, 'Br': 16, '[K+]': 17, '[O-]': 18, 'F': 19, '[H-]': 20, '[H]': 21, '[Na+]': 22, '[NH3+]': 23, '[NH+]': 24, '[nH]': 25, '4': 26, 'S': 27, '[NH2+]': 28, 'Cl': 29, '-': 30, 'o': 31, '[Br-]': 32, '[Mg+]': 33, '#': 34, '5': 35, '[I-]': 36, 'P': 37, '6': 38, '[Li+]': 39, '[N-]': 40, 's': 41, '[n+]': 42, '[N+]': 43, '[Na]': 44, '[F-]': 45, '[Si]': 46, '[Pd]': 47, '[NH4+]': 48, 'I': 49, '[nH+]': 50, '[BH4-]': 51, '[Cu]': 52, '[Al+3]': 53, '[Cs+]': 54, '[Pd+2]': 55, '[BH3-]': 56, 'B': 57, '[S-]': 58, '[PH+]': 59, '7': 60, '[P-]': 61, '[K]': 62, '[Fe]': 63, '[SiH]': 64, '[BH-]': 65, '[Mn]': 66, '[Cu+2]': 67, '[Pt]': 68, '[Zn]': 69, '[O+]': 70, '[B-]': 71, '[n-]': 72, '8': 73, '[CH-]': 74, '[GeH4]': 75, '[Zn+2]': 76, '[Mg]': 77, '[Cr]': 78, '[W]': 79, '[Sn]': 80, '[Ca+2]': 81, '[P+]': 82, '[Ca]': 83, '[Zn+]': 84, '[Se]': 85, '[Al]': 86, '[S+]': 87, '9': 88, '%10': 89, '[Co]': 90, '[SH-]': 91, '[Ag+]': 92, '[Yb+3]': 93, '[Fe+2]': 94, '[Mg+2]': 95, '[PH]': 96, '[SnH]': 97, '[se]': 98, '[Ni]': 99, '[Hg]': 100, '[SiH2]': 101, '[Au]': 102, '[Pb]': 103, '[Co+2]': 104, '[Cr+2]': 105, '[SH]': 106, '[C-]': 107, '[SiH3]': 108, '[As]': 109, '[Fe+3]': 110, '[Ti]': 111, '[H+]': 112, '[IH2]': 113, '[OH+]': 114, '[Cd+2]': 115, '[Ba+2]': 116, '[NH-]': 117, '[Os]': 118, '[In+3]': 119, '[Ni+2]': 120, '[cH-]': 121, '[TeH2]': 122, '[Ce+3]': 123, '%11': 124, '%12': 125, '%13': 126, '[Mn+2]': 127, '[Ce]': 128, '[Cr+3]': 129, '[In]': 130, '[Rh]': 131, '[GeH]': 132, '[Ge]': 133, '[Bi]': 134, '[Ir]': 135, '[Pb+2]': 136, '[Cs]': 137, '[Ag]': 138, '[Cd]': 139, '[c-]': 140, '[SiH4]': 141, '[Ru]': 142, '[Sc+3]': 143, '[V]': 144, '[V+3]': 145, '[Ar]': 146, '[Ba]': 147, '[Sn+]': 148, '[Mo]': 149, '[Xe]': 150, '[Sn+2]': 151, '[Y+3]': 152, 'p': 153, '[Sb]': 154, '%14': 155, '%15': 156, '[Se-]': 157, '[Tl]': 158, '[He]': 159, '[Dy+3]': 160, '[SeH]': 161, '[Sr+2]': 162, '[Sr]': 163, '[Tl+3]': 164, '[Sm]': 165, '[Ga+3]': 166, '[s+]': 167, '[Ta]': 168, '[Mn+3]': 169, '[Be+2]': 170, '[La+3]': 171, '[Ga]': 172, '[Re]': 173, '[o+]': 174, '[SeH-]': 175, '[Zr]': 176, '[Tl+]': 177, 'b': 178, '[Sc]': 179, '[Nd+3]': 180, '[Co+3]': 181, '[As+]': 182, '[Rb+]': 183, '[se+]': 184, '[Sm+3]': 185, '[Hf]': 186, '[Pr+3]': 187, '[GeH2]': 188, '[Au-]': 189, '[Yb]': 190, '[C+]': 191, 'pad': 0, 'SOS': 192}

smi = "c1(c(C([O-])=O)c(c([nH]1)C=O)C)C.n1(ccnn1)CC[NH3+]>>n1(ccnn1)CCNC(c2c([nH]c(c2C)C=O)C)=O"
pred = Prediction(smi, vocabulary)
matrix = pred.get_matrix()
print(matrix)
#arr = pred.get_data()

inputs, out = matrix
print(inputs)
print(out)
enc_inp, tar_inp, tar_out = inputs
print(enc_inp)
print(tar_inp)
print(tar_out)

