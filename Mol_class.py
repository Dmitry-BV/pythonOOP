class Molecule:
    def __init__(self):
        self._atoms = {}
        self._bonds = {}
        self._atoms_table = {"H": [1], "HE": [1], "LI": [1], "BE": [1, 2], "B": [1], "C": [1, 2, 3], "N": [1, 2, 3],
                             "O": [1, 2], "CL": [1], "NA": [1], "K": [1], "F": [1], "BR": [1], "FE": [2, 3]}

    def validation(self, *, atom=None, map_=None, bond=None, if_exists=None):
        """
        Проверка корректности ввода
        """
        if atom is not None:  # Проверка ввода атома
            if not isinstance(atom, str):
                raise TypeError("Not a string!")
            if atom.upper() not in self._atoms_table:
                raise ValueError("Wrong atom!")
        if map_ is not None:  # Проверка ввода номера атома при добавлении или удалении атома
            if not isinstance(map_, int):
                raise TypeError
            elif map_ < 1:
                raise ValueError
        if bond is not None:  # Проверка ввода типа связи
            if not isinstance(bond, int):
                raise TypeError
            if bond not in (1, 2, 3):
                raise ValueError
            if bond not in self._atoms_table[self._atoms[map_].upper()] or \
                    bond not in self._atoms_table[self._atoms[map_].upper()]:
                raise TypeError("Bad valence!")
        if if_exists is not None:  # Проверка номера при удалении атома или связи между двумя атомами
            if if_exists not in self._atoms:
                raise ValueError("Atom with this number is not exists!")

    def add_atom(self, atom, map_=None):
        """
        Добавление атома
        map_ - номер атома
        """
        if map_ is None:
            map_ = max(self._atoms, default=0) + 1
        elif map_ in self._atoms:
            raise KeyError
        self.validation(atom=atom, map_=map_)
        self._atoms[map_] = atom
        self._bonds[map_] = {}
        return map_  # отображение номера атома

    def del_atom(self, map_):
        """
        Удаление атома
        """
        self.validation(map_=map_, if_exists=map_)
        del self._atoms[map_]
        del self._bonds[map_]
        for value in self._bonds.values():
            if map_ in value:
                del value[map_]
        return map_

    def add_bond(self, map1, map2, bond):
        self.validation(map_=map1, bond=bond)
        self.validation(map_=map2, bond=bond)

        # есть ли в селф.атом, что мап1 не равно мап2, что уже есть связь м\у этими атомами, что одноатомн мол-ла
        neigh1 = self._bonds[map1]
        neigh2 = self._bonds[map2]

        if neigh1 is neigh2:  # map1 не равно map2 (атом с самим собой)
            raise KeyError
        if map1 in neigh2:  # если связь уже существует, raise Error
            raise KeyError

        neigh1[map2] = bond
        neigh2[map1] = bond

    def del_bond(self, map1, map2):
        self.validation(map_=map1, if_exists=map1)
        self.validation(map_=map2, if_exists=map2)
        for value in self._bonds.values():
            if map1 in value:
                del value[map1]
            if map2 in value:
                del value[map2]

    def show_atoms(self):
        return self._atoms.copy()

    def show_bonds(self):
        return self._bonds.copy()


ol = Molecule()
ol.add_atom("C")
ol.add_atom("c")
ol.add_atom("N")
ol.add_atom("n")
ol.add_atom("O")
ol.add_atom("o")
print("Добавление атомов:")
print(ol.show_atoms())
ol.add_bond(1, 2, 1)
ol.add_bond(2, 3, 1)
ol.add_bond(3, 4, 1)
ol.add_bond(3, 5, 2)
ol.add_bond(6, 4, 1)
ol.add_bond(6, 5, 2)
print("Добавление связей:")
print(ol.show_bonds())
ol.del_bond(1, 2)
print("Удаление связи между 1 и 2")
print(ol.show_bonds())
print(ol.show_atoms())
print("Удаление атома под номером 2:")
ol.del_atom(2)
print(ol.show_bonds())
print(ol.show_atoms())
