def safe_ascii():
    bang = ord("!")
    ampersand = ord("&") - 4
    openSquareBracket = ord("[") - 56
    underscore = ord("_") - 59
    a = ord("a") - 60
    tilde = ord("~")

    def encode(n):
        if n == 0:
            return bang
        if n < 5:
            return n + ampersand
        if n < 57:
            return n + openSquareBracket
        if n < 60:
            return n + underscore
        if n < 89:
            return n + a
        return tilde

    return encode
