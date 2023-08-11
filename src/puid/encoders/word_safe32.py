# n: 01234567 8 901 2 3 456 789 0 123 4 5 678 901
# c: 23456789 C FGH J M PQR VWX c fgh j m pqr vwx

def word_safe32():
    def encoder(n):
        two = ord("2")
        C = ord("C")
        F = ord("F")
        J = ord("J")
        M = ord("M")
        P = ord("P")
        V = ord("V")
        c = ord("c")
        f = ord("f")
        j = ord("j")
        m = ord("m")
        p = ord("p")
        v = ord("v")

        if (n < 8):
            return n + two
        if (n == 8):
            return C
        if (n < 12):
            return n - 9 + F
        if (n == 12):
            return J
        if (n == 13):
            return M
        if (n < 17):
            return n - 14 + P
        if (n < 20):
            return n - 17 + V
        if (n == 20):
            return c
        if (n < 24):
            return n - 21 + f
        if (n == 24):
            return j
        if (n == 25):
            return m
        if (n < 29):
            return n - 26 + p
        return n - 29 + v

    return encoder
