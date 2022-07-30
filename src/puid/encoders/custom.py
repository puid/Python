def custom(chars):
    char_codes = [ord(char) for char in chars.value]
    return lambda n: char_codes[n]
