def safe64():
    upper = ord("A")
    lower = ord("a") - 26
    decimal = ord("0") - 52
    hyphen = ord("-")
    underscore = ord("_")

    def encoder(n):
        if n < 26:
            return n + upper
        if n < 52:
            return n + lower
        if n < 62:
            return n + decimal
        if n == 62:
            return hyphen
        return underscore

    return encoder
