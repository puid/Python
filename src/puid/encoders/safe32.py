def safe32():
    two = ord("2")
    six = ord("6") - 3
    b = ord("b")
    d = ord("d")
    f = ord("f") - 9
    j = ord("j")
    m = ord("m") - 13
    p = ord("p") - 15
    t = ord("t")
    B = ord("B")
    D = ord("D")
    F = ord("F") - 21
    J = ord("J")
    L = ord("L") - 25
    P = ord("P") - 28
    T = ord("T")

    def encoder(n):
        if n < 3:
            return n + two
        if n < 7:
            return n + six
        if n == 7:
            return b
        if n == 8:
            return d
        if n < 12:
            return n + f
        if n == 12:
            return j
        if n < 15:
            return n + m
        if n < 18:
            return n + p
        if n == 18:
            return t
        if n == 19:
            return B
        if n == 20:
            return D
        if n < 24:
            return n + F
        if n == 24:
            return J
        if n < 28:
            return n + L
        if n < 31:
            return n + P
        return T

    return encoder
