def base32():
    alpha = ord("A")
    decimal = ord("2") - 26

    def encoder(n):
        return n + (alpha if n < 26 else decimal)

    return encoder


def base32_hex():
    return _base32_hex_case(False)


def base32_hex_upper():
    return _base32_hex_case(True)


def _base32_hex_case(upper):
    decimal = ord("0")
    alpha = (ord("A") if upper else ord("a")) - 10

    def encoder(n):
        return n + (decimal if n < 10 else alpha)

    return encoder
