def base16():
    decimal = ord("0")
    alpha = ord("A")

    def encoder(n):
        if (n < 10):
            return n + decimal
        return n - 10 + alpha

    return encoder
