from random import gauss
"""
Example of inheritance
"""

class CustomFloat:
    def __int__(self):
        return int(float(self))

    def __add__(self, other):
        """
        Суммирование
        :param other:
        :return: float
        """
        if isinstance(other, CustomFloat):
            other = float(other)
        elif not isinstance(other, (float, int)):
            raise TypeError("Not float")
        return float(self) + other

    def __radd__(self, other):
        return self + other


class RandomFloat(CustomFloat):
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
        return f"{float(self)}"

    def __iadd__(self, other):
        if isinstance(other, RandomFloat):
            return float(RandomFloat(self.mu + other.mu))
        if not isinstance(other, (int, float)):
            raise TypeError
        return float(RandomFloat(self.mu + other))

    def __isub__(self, other):
        if isinstance(other, RandomFloat):
            return float(RandomFloat(self.mu - other.mu))
        if not isinstance(other, (int, float)):
            raise TypeError
        return float(RandomFloat(self.mu - other))


class EpsilonFloat(CustomFloat):
    def __init__(self, /, data, *, epsilon=1e-5):
        if not isinstance(data, (float, RandomFloat)) or not isinstance(epsilon, (int, float)):
            raise TypeError("Wrong Type")
        if epsilon < 0:
            raise ValueError("Negative Value for Epsilon!")
        self.data = data
        self.epsilon = epsilon

    def __float__(self):
        return self.data

    def __repr__(self):
        return f"{float(self.data)}"

    def __eq__(self, other):
        if not isinstance(other, (int, float, EpsilonFloat)):
            raise TypeError("WrongType!")
        if float(other) - self.epsilon < self.data < float(other) + self.epsilon:
            return True
        else:
            return False

    def __iadd__(self, other):
        if isinstance(other, EpsilonFloat):
            return float(EpsilonFloat(self.data + other.data))
        if not isinstance(other, (int, float)):
            raise TypeError
        return float(EpsilonFloat(self.data + other))

    def __isub__(self, other):
        if isinstance(other, EpsilonFloat):
            return float(EpsilonFloat(self.data - other.data))
        if not isinstance(other, (int, float)):
            raise TypeError
        return float(EpsilonFloat(self.data - other))

    def __imul__(self, other):
        if isinstance(other, EpsilonFloat):
            return float(EpsilonFloat(self.data * other.data))
        if not isinstance(other, (int, float)):
            raise TypeError
        return float(EpsilonFloat(self.data * other))


rf = RandomFloat(10.)
rf2 = RandomFloat(10.)
print("RandomFloat 1:", rf)
print("RandomFloat 2:", rf2)
print("RF1 == 10:", rf == 10)
print("RF1 == RF2:", rf == rf2)
rf -= rf2
print("RF1 -= RF2", rf)

ef = EpsilonFloat(10.0, epsilon=2)
ef2 = EpsilonFloat(15.0)
print("EpsilonFloat 1:", ef)
print("EpsilonFloat 2:", ef2)
print("EF1 == 10, eps.=2:", ef == 10)
print("EF1 == EF2, eps.=2:", ef == ef2)
print("EF2 == EF2", ef2 == ef2)
ef += ef2
print("EF1 += EF2", ef)
ef *= 10
print("EF1 *= 10:", ef)