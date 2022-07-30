def alpha():
    upper = ord("A")
    lower = ord("a") - 26

    return lambda n: n + (upper if n < 26 else lower)


def alpha_lower():
    return _alpha_case(False)


def alpha_upper():
    return _alpha_case(True)


def _alpha_case(upper):
    alpha = ord("A") if upper else ord("a")
    return lambda n: n + alpha
