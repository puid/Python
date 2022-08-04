def alphanum():
    upper = ord("A")
    lower = ord("a") - 26
    decimal = ord("0") - 52

    def encoder(n):
        if n < 26:
            return n + upper
        if n < 52:
            return n + lower
        return n + decimal

    return encoder


def alphanum_lower():
    return _alphanum_case(False)


def alphanum_upper():
    return _alphanum_case(True)


def _alphanum_case(upper):
    alpha = ord("A") if upper else ord("a")
    decimal = ord("0") - 26

    def encoder(n):
        return n + (alpha if n < 26 else decimal)

    return encoder
