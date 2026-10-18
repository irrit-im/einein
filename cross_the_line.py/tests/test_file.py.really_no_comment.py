



























def add_three(num):
    return num + 3


if __name__ == "__main__":
    g1 = Functor(mod_three)  
    g2 = Functor(add_three)
    g3 = g1 + g2  
    print(g3(5))
    print(g3(5) + 2)
    g4 = g1 * 3
    print(g4(4))
    g5 = g1 * g2
    print(g5(5))
