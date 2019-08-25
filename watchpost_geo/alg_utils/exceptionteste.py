
# def abc():
#     try:
#         raise Exception("criando o exception", 'abc')
#     except Exception as e:
#         print('e', e)
#         print('args:', e.args)
#         raise Exception(10, e.args[0])
#
# try:
#     print(abc())
# except Exception as e:
#     print(e)


class Tonto(Exception):
    def __str__(self):
        return "bbbb"


def t():
    try:
        raise Tonto('aaa')
    except Tonto as t:  # Se chamarmos a superclasse antes vai dar ruim
        print('t', t.args)
    except Exception as e:
        print(e)

t()