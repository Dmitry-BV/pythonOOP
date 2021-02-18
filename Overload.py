import math
from random import gauss

class Class:
    def __init__(self, var):
        if not isinstance(var, str):
            raise TypeError('Not String')
        if not var:
            raise ValueError

        self.var = var
        self.blah = {}

    def set_blah(self, data, /):
        if not isinstance(data, dict):
            raise TypeError
        if any(not isinstance(x, str) for x in data):
            raise TypeError('Not String in keys')
        if any(not x for x in data):
            raise ValueError
        self.blah = data.copy()

    def get_blah(self):
        return self.blah.copy()


class RandomFloat:
    """
    Пример перегрузки операторов
    """
    def __init__(self, mu: float, /, *, sigma: float = 1.):
        if not isinstance(mu, float) or not isinstance (sigma, float):
            raise TypeError
        self.mu = mu
        self.sigma = sigma

    def __float__(self):
        # return self.mu
        return gauss(self.mu, self.sigma)

    def __int__(self):
        return int(float(self))

    def __add__(self, other):
        """
        Суммирование
        :param other:
        :return: float
        """
        if isinstance(other, RandomFloat):
            other = float(other)
        elif not isinstance(other, (float, int)):
            raise TypeError("Not float")
        return float(self) + other

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        """
        Вычитание
        :param other:
        :return: float
        """
        if isinstance(other, RandomFloat):
            other = float(other)
        elif not isinstance(other, (float, int)):
            raise TypeError("Not float")
        return float(self) - other

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        """
        Умножение
        :param other:
        :return: float
        """
        if isinstance(other, RandomFloat):
            other = float(other)
        elif not isinstance(other, (float, int)):
            raise TypeError("Not float")
        return float(self) * other

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        """
        Деление x / y
        :param other:
        :return: float
        """
        if isinstance(other, RandomFloat):
            other = float(other)
        elif not isinstance(other, (float, int)):
            raise TypeError("Not float")
        return float(self) / other

    def __rtruediv__(self, other):
        return other / float(self)

    def __floordiv__(self, other):
        """
        Целочисленное деление x // y
        :param other:
        :return: float
        """
        if isinstance(other, RandomFloat):
            other = float(other)
        elif not isinstance(other, (float, int)):
            raise TypeError("Not float")
        return float(self) // other

    def __rfloordiv__(self, other):
        return other // float(self)

    def __mod__(self, other):
        """
        Остаток от деления x % y
        :param other:
        :return: float
        """
        if isinstance(other, RandomFloat):
            other = float(other)
        elif not isinstance(other, (float, int)):
            raise TypeError("Not float")
        return float(self) % other

    def __rmod__(self, other):
        return other % float(self)

    def __lt__(self, other):
        """
        Сравнение x < y (less than)
        :param other:
        :return: Bool
        """
        if isinstance(other, RandomFloat):
            other = float(other)
        elif not isinstance(other, (float, int)):
            raise TypeError("Not float")
        return float(self) < other

    def __gt__(self, other):
        """
        Сравнение x > y (greater than)
        :param other:
        :return: Bool
        """
        if isinstance(other, RandomFloat):
            other = float(other)
        elif not isinstance(other, (float, int)):
            raise TypeError("Not float")
        return float(self) > other

    def __eq__(self, other):
        """
        Сравнение x == y (equal)
        :param other:
        :return: Bool
        """
        if isinstance(other, RandomFloat):
            other = float(other)
        elif not isinstance(other, (float, int)):
            raise TypeError("Not float")
        return float(self) == other

    def __neg__(self):
        """
        Унарный минус (negative)
        :return: float
        """
        return -float(self)

    def __pos__(self):
        """
        Унарный плюс (positive)
        :return: float
        """
        return +float(self)

    def __abs__(self):
        """
        Получение абсолютного значения (abs)
        :return: float
        """
        return abs(float(self))

    def __round__(self, n=None):
        """
        Округление
        :param n: int
        :return: int
        """
        if not isinstance(n, int):
            raise TypeError("Not Integer")
        return round(float(self), n)

    def __pow__(self, power):
        """
        Power
        :param power: int, float
        :return: float
        """
        if isinstance(power, RandomFloat):
            power = float(power)
        elif not isinstance(power, (float, int)):
            raise TypeError("Not float")
        return float(self) ** power

    def __rpow__(self, power):
        return power ** float(self)

    def __repr__(self):
        """
        Получение текстового описания объекта (reputation)
        :return: str
        """
        return f"{float(rf)}"

    def __iadd__(self, other):
        if isinstance(other, RandomFloat):
            return float(self.mu + other.mu)
        if not isinstance(other, (int, float)):
            raise TypeError
        return float(self.mu + other)


rf = RandomFloat(10.)
"""
rf_list = list()
for i in range(10):
    rf_list.append(int(rf))
print(rf_list)
print(mean(rf_list))
"""

print("Суммирование - Add:", rf + 10)
print("Суммирование - RAdd:", 10 + rf)
print("Вычитание - Sub:", rf - 5)
print("Вычитание - RSub:", 5 - rf)
print("Умножение - Mul:", rf * 10)
print("Умножение - RMul:", 10 * rf)
print("Деление - TrueDiv:", rf / 5)
print("Деление - RTrueDiv:", 5 / rf)
print("Целочисленное деление - FloorDiv:", rf // 5)
print("Целочисленное деление - RFloorDiv:", 5 // rf)
print("Остаток от деления - Mod:", rf % 5)
print("Остаток от деления - RMod:", 5 % rf)
print("Сравнение - Less Than (lt):", rf < 5)
print("Сравнение - Greater Than (gt):", 5 < rf)
print("Сравнение - Equal (eq):", rf == 10.0)
print("Унарный минус:", -rf)
print("Унарный плюс:", +rf)
print("Абсолютное значение - Abs:", abs(rf))
print("Булево значение - Bool:", bool(rf))
print("Округление (round) до второго знака:", round(rf, 2))
print("Power - Pow:", pow(rf, 2))
print("Power - RPow:", pow(2, rf))
print("Floor:", math.floor(rf))
print("Ceil:", math.ceil(rf))
print("Строковое представление объекта - Repr:", rf)

c = RandomFloat(10.)
print(c)
c += 20.
print(c)
"""
rf_inc = (RandomFloat(10.),)
print(rf_inc, rf_inc[0].mu)
try:
    rf_inc[0] += 1
except:
    pass
print(rf_inc, rf_inc[0].mu)
"""

# print(rf.__hash__())