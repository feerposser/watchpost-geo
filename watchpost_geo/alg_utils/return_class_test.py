
class T:
    def __init__(self, t):
        self.t = t

    def __str__(self):
        return "--t: %s" % self.t

    def retorno(self):
        return {'t': self.t}

    def is_same(self, t):
        if isinstance(t, T):
            print(True)
        else:
            print(False)


t = T('a').retorno()
print(t)