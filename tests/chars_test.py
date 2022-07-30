import pytest

from puid import Chars
from puid.chars import CustomChars
from puid.chars import PredefinedChars
from puid.chars import valid_chars
from puid.chars_error import InvalidChars
from puid.chars_error import NonUniqueChars
from puid.chars_error import TooFewChars
from puid.chars_error import TooManyChars


def predefined_chars():
    return [
        Chars.ALPHA,
        Chars.ALPHA_LOWER,
        Chars.ALPHA_UPPER,
        Chars.ALPHANUM,
        Chars.ALPHANUM_LOWER,
        Chars.ALPHANUM_UPPER,
        Chars.BASE32,
        Chars.BASE32_HEX,
        Chars.BASE32_HEX_UPPER,
        Chars.DECIMAL,
        Chars.HEX,
        Chars.HEX_UPPER,
        Chars.SAFE32,
        Chars.SAFE64,
        Chars.SAFE_ASCII,
        Chars.SYMBOL,
    ]


def test_chars_too_short():
    with pytest.raises(TooFewChars):
        valid_chars("a")


def test_chars_too_long():
    with pytest.raises(TooManyChars):
        valid_chars("".join(["a"] * 257))


def test_chars_not_unique():
    with pytest.raises(NonUniqueChars):
        valid_chars("unique")


def test_invalid_chars():
    with pytest.raises(InvalidChars):
        valid_chars("dingosky\n")

    with pytest.raises(InvalidChars):
        valid_chars("dingosky'")

    with pytest.raises(InvalidChars):
        valid_chars('dingosky"')

    with pytest.raises(InvalidChars):
        valid_chars('dingosky`')

    with pytest.raises(InvalidChars):
        valid_chars("dingosky\\")

    with pytest.raises(InvalidChars):
        valid_chars("dingosky" + chr(ord("~") + 2))


def test_chars_not_valid():
    with pytest.raises(InvalidChars):
        valid_chars(3)


def test_predefined_chars():
    for chars in predefined_chars():
        assert valid_chars(chars)


def test_predefined_chars_object():
    alpha = PredefinedChars(Chars.ALPHA)
    assert len(alpha) == 52


def test_invalid_predefined_chars_object():
    with pytest.raises(InvalidChars):
        PredefinedChars('dingosky')


def test_custom_chars_object():
    dingosky = CustomChars('dingosky')
    assert len(dingosky) == 8


def test_invalid_custom_chars_object():
    with pytest.raises(InvalidChars):
        CustomChars(Chars.ALPHA)


def test_predefined_chars_values():
    for value in [chars.value for chars in predefined_chars()]:
        assert valid_chars(value)


def test_chars_repr():
    assert PredefinedChars(Chars.HEX).__repr__() == "HEX -> '0123456789abcdef'"


def test_chars_iter():
    assert [char for char in CustomChars('dingosky')] == list('dingosky')
