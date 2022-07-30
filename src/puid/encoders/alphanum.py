def alphanum():
    decimal = ord("0")
    upper = ord("A") - 10
    lower = ord("a") - 36

    def encoder(n):
        if n < 10:
            return n + decimal
        if n < 36:
            return n + upper
        return n + lower

    return encoder


def alphanum_lower():
    return _alphanum_case(False)


def alphanum_upper():
    return _alphanum_case(True)


def _alphanum_case(upper):
    decimal = ord("0")
    alpha = (ord("A") if upper else ord("a")) - 10

    return lambda n: n + (decimal if n < 10 else alpha)
