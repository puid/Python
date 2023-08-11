# n: 0123456789 01234567 89 01 23456 78901
# c: 0123456789 ABCDEFGH JK MN PQRST VWXYZ

def crockford32():
    zero = ord("0")
    A = ord("A")
    J = ord("J")
    M = ord("M")
    P = ord("P")
    V = ord("V")

    def encoder(n):
        if (n < 10):
            return n + zero
        if (n < 18):
            return n - 10 + A
        if (n < 20):
            return n - 18 + J
        if (n < 22):
            return n - 20 + M
        if (n < 27):
            return n - 22 + P
        return n - 27 + V

    return encoder
