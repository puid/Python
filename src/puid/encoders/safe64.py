def safe64():
    decimal = ord("0")
    upper = ord("A") - 10
    lower = ord("a") - 36
    hyphen = ord("-")
    underscore = ord("_")

    def encoder(n):
        if n < 10:
            return n + decimal
        if n < 36:
            return n + upper
        if n < 62:
            return n + lower
        if n == 62:
            return hyphen
        return underscore

    return encoder
