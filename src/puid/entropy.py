from math import ceil
from math import log2
from math import trunc

from puid.chars import ValidChars
from puid.chars_error import InvalidChars
from puid.puid_error import TotalRiskError


def bits_for_total_risk(total: 0, risk: 0):
    """
    Entropy bits necessary to produce a `total` `puid`s with given `risk` of repeat

    :param total: int
    :param risk: int
    :return float

    >>> bits_for_total_risk(100_000, 1e12)
    72.08241808752197
    """

    def non_neg_int_or_float(value):
        if isinstance(value, int) and 0 <= value:
            return True
        if isinstance(value, float) and value.is_integer() and 0.0 <= value:
            return True
        return False

    if not non_neg_int_or_float(total) or not non_neg_int_or_float(risk):
        raise TotalRiskError('total and risk must be an non-negative integers')

    if total in [0, 1]:
        return 0

    if risk in [0, 1]:
        return 0

    if total < 1000:
        return log2(total) + log2(total - 1) + log2(risk) - 1
    else:
        return 2 * log2(total) + log2(risk) - 1


def bits_per_char(chars):
    """
    Entropy bits per character for either a predefined Chars enum or a string of characters

    :param chars: Either a Chars enum or a string

    raises CharsError subclass if `chars` is invalid

    >>> bits_per_char(Chars.BASE32)
    5.0

    >>> bits_per_char('dingosky_me')
    3.4594316186372973
    """
    if isinstance(chars, ValidChars):
        return log2(len(chars))
    else:
        raise InvalidChars('chars must be an instance of ValidChars')


def bits_for_len(chars, len):
    """
    Bits necessary for a `puid` of length `len` using characters `chars`

    :param chars: Either a Chars enum or a string
    :param len: Desired length of `puid`

    raises CharsError subclass if `chars` is invalid

    >>> bits_for_len('dingosky', 14)
    42
    """
    return trunc(len * bits_per_char(chars))


def len_for_bits(chars, bits):
    """
    Length necessary for a `puid` of `bits` using characters `chars`

    :param chars: Either a Chars enum or a string
    :param bits: Desired `bits` of `puid`

    raises CharsError subclass if `chars` is invalid

    >>> len_for_bits(Chars.SAFE_ASCII, 97)
    15
    """
    return ceil(bits / bits_per_char(chars))


if __name__ == '__main__':  # pragma: no cover
    import doctest

    doctest.testmod()
