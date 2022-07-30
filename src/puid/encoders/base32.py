def base32():
    decimal = ord("2")
    alpha = ord("A") - 6

    return lambda n: n + (decimal if n < 6 else alpha)


def base32_hex():
    return _base32_hex_case(False)


def base32_hex_upper():
    return _base32_hex_case(True)


def _base32_hex_case(upper):
    decimal = ord("0")
    alpha = (ord("A") if upper else ord("a")) - 10

    return lambda n: n + (decimal if n < 10 else alpha)
