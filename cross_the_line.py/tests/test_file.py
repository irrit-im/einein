# class Functor:
#     def __init__(self, func: callable) -> "Functor":
#         self.func = func

#     def __call__(self, arg):
#         return self.func(arg)

#     def __add__(self, other):
#         if isinstance(other, Functor):
#             return Functor(lambda x: self(x) + other(x))

#     def __sub__(self, other):
#         if isinstance(other, Functor):
#             return Functor(lambda x: self(x) - other(x))
#         else:
#             return self - other

#     def __mul__(self, other):
#         if isinstance(other, Functor):
#             return Functor(lambda x: self(other(x)))
#         else:
#             return lambda x: self(x) * other


# def mod_three(num):
#     return num % 3


def add_three(num):
    return num + 3


if __name__ == "__main__":
    g1 = Functor(mod_three)  # rrhgohjfioj
    g2 = Functor(add_three)
    g3 = g1 + g2  # oghio;gjlojlfdo
    print(g3(5))
    print(g3(5) + 2)
    g4 = g1 * 3
    print(g4(4))
    g5 = g1 * g2
    print(g5(5))
