from enum import Enum

from puid.chars_error import InvalidChars, NonUniqueChars, TooFewChars, TooManyChars


def valid_chars(chars):
    """
    Tests whether characters are valid.

    raises A CharsError subclass if characters are not valid.

    >>> valid_chars(Chars.HEX)
    True

    >>> valid_chars('dingosky')
    True
    """
    if isinstance(chars, Chars):
        return True

    if not isinstance(chars, str):
        raise InvalidChars('Characters must be a str')

    min_len = 2
    max_len = 256

    if len(chars) < min_len:
        raise TooFewChars(f'Must have at least {min_len} characters')

    if 256 < len(chars):
        raise TooManyChars(f'Exceeded max of {max_len} characters')

    if len(chars) != len(set(chars)):
        raise NonUniqueChars('Characters are not unique')

    for char in chars:
        if not _valid_char(char):
            raise InvalidChars(f'Invalid character with code: {ord(char)}')

    return True


def _valid_char(char):
    code_point = ord(char)

    if 160 < code_point:
        return True

    if char == '!':
        return True
    if code_point < ord('#'):
        return False
    if char == "'":
        return False
    if char == '\\':
        return False
    if char == '`':
        return False
    if ord('~') < code_point:
        return False

    return True


class Chars(Enum):
    """
    Predefined Characters

    These enums are intended to be passed to the `Puid` class initializer for configuration
    """

    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ALPHA_LOWER = 'abcdefghijklmnopqrstuvwxyz'
    ALPHA_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ALPHANUM = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    ALPHANUM_LOWER = 'abcdefghijklmnopqrstuvwxyz0123456789'
    ALPHANUM_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    BASE16 = '0123456789ABCDEF'
    BASE32 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
    BASE32_HEX = '0123456789abcdefghijklmnopqrstuv'
    BASE32_HEX_UPPER = '0123456789ABCDEFGHIJKLMNOPQRSTUV'
    CROCKFORD32 = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
    DECIMAL = '0123456789'
    HEX = '0123456789abcdef'
    HEX_UPPER = '0123456789ABCDEF'
    SAFE_ASCII = '!#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}~'
    SAFE32 = '2346789bdfghjmnpqrtBDFGHJLMNPQRT'
    SAFE64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    SYMBOL = '!#$%&()*+,-./:;<=>?@[]^_{|}~'
    WORD_SAFE32 = '23456789CFGHJMPQRVWXcfghjmpqrvwx'

    def __len__(self):
        return len(self.value)


class ValidChars:
    """Base class for PredefinedChars and CustomChars"""

    def __repr__(self):
        return "{0} -> '{1}'".format(self.name, self.value)

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)


class PredefinedChars(ValidChars):
    """
    Class for Predefined Chars

    raises InvalidChars if initialized with anything other than a predefined Chars enum

    >>> hex_upper = PredefinedChars(Chars.HEX_UPPER)

    This class is intended for internal use
    """

    def __init__(self, chars):
        """
        Create a PredefinedChars for Chars enum

        :param chars: Chars enum
        """
        if isinstance(chars, Chars):
            self.name = chars.name
            self.value = chars.value
        else:
            raise InvalidChars('PredefinedChars only accepts members of the Chars enum')


class CustomChars(ValidChars):
    """
    Class for Custom Chars

    raises CharsError if initialized with an string of characters that are invalid
    raises InvalidChars if initialized with a predefined Chars enum

    >>> dingosky = CustomChars('dingosky')

    This class is intended for internal use
    """

    def __init__(self, chars):
        """
        Create a CustomChars for a string of characters

        :param chars: A valid string of characters
        """
        if isinstance(chars, Chars):
            raise InvalidChars('Use class PredefinedChars for members of the Chars enum')
        else:
            valid_chars(chars)
            self.name = 'Custom'
            self.value = chars


if __name__ == '__main__':  # pragma: no cover
    import doctest

    doctest.testmod()
