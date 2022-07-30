def _hex_case(upper):
    decimal = ord("0")
    alpha = (ord("A") if upper else ord("a")) - 10

    def encoder(n):
        if n < 10:
            return n + decimal
        return n + alpha

    return encoder


def hex_lower():
    return _hex_case(False)


def hex_upper():
    return _hex_case(True)
