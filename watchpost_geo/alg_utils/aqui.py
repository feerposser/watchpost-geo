class A:
    b = 'b'
    def __init__(self):
        self.a = 'a'
        self.__l = 'l'

    def tes(self):
        print('tes:', self.a)

a = A()
print(a.a)
print(a.b)

A().tes()

print(a.l)
