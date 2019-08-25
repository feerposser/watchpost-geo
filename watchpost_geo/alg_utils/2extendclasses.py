class A:
    def __init__(self, a):
        self.a = a
        print('a')

    def aa(self):
        print('-->', self.a)


class B:
    def __init__(self, b):
        self.b = b
        print('b')

    def bb(self):
        print('-->', self.b)


class C(A, B):
    def __init__(self, c):
        B.__init__(self, 'b')
        A.__init__(self, 'a')
        # super().__init__(c)
        # self.b = c


c = C('c')

c.bb()
c.aa()
