import time


class A():
    def __init__(self):
        pass

    def io(self) -> None:
        for _ in range(10):
            time.sleep(1)
            print("i", end="")

    def fibo(self, n: int=6) -> int:
        if n<=1: 
            return(1)
        else: return self.fibo(n-1) + self.fibo(n-2)

    def facto(self, n: int = 100000000, p: int = int(1E9+7)):
        a = 1
        for i in range(1, n):
            a = (a*i)%p
        return a


def ffibo(n: int=35) -> int:
    if n<=1: 
        return(1)
    else: return ffibo(n-1) + ffibo(n-2)

def facto(n: int = 100000000, p: int = int(1E9+7)):
    a = 1
    for i in range(1, n):
        a = (a*i)%p
    return a

