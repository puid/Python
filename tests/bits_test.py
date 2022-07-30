from puid import Chars
from puid.bits import bit_shifts
from puid.chars import CustomChars
from puid.chars import PredefinedChars


def check_predefined(chars, shifts):
    n_chars = len(PredefinedChars(chars))
    assert bit_shifts(n_chars) == shifts


def test_bit_shifts_pow_2():
    assert bit_shifts(len(CustomChars('dingosky'))) == [(8, 3)]
    check_predefined(Chars.HEX, [(16, 4)])
    check_predefined(Chars.BASE32_HEX_UPPER, [(32, 5)])
    check_predefined(Chars.SAFE64, [(64, 6)])


def test_bit_shifts_non_pow_2():
    check_predefined(Chars.ALPHA, [(52, 6), (55, 5), (63, 3)])
    check_predefined(Chars.ALPHA_LOWER, [(26, 5), (31, 3)])
    check_predefined(Chars.ALPHANUM_LOWER, [(36, 6), (39, 5), (47, 3), (63, 2)])
    check_predefined(Chars.SAFE_ASCII, [(90, 7), (95, 5), (127, 2)])
