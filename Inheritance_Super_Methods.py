class W:
    def x(self):
        print('W')


class E(W):
    def x(self):
        print('E')
        super().x()


class A(E):
    def x(self):
        print('A')
        super().x()


class B(W):
    def x(self):
        print('B')
        super().x()


class C(A, B):
    def x(self):
        print('C')
        super().x()

c = C()
print(c.x())