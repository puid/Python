import pytest

from puid import Chars
from puid.chars import CustomChars
from puid.chars import PredefinedChars
from puid.chars_error import InvalidChars
from puid.entropy import bits_for_len
from puid.entropy import bits_for_total_risk
from puid.entropy import bits_per_char
from puid.entropy import len_for_bits
from puid.puid_error import TotalRiskError


@pytest.mark.parametrize("total, risk", [(0, 1e8), (1, 100), (100, 0), (1000, 1)])
def test_bits_for_total_risk_is_0(total, risk):
    assert bits_for_total_risk(total, risk) == 0.0


@pytest.mark.parametrize("total, risk", [(-1, 0), (0, -1), ('a', 0), (1000, [])])
def test_bits_for_invalid_total_risk(total, risk):
    with pytest.raises(TotalRiskError):
        bits_for_total_risk(total, risk)


@pytest.mark.parametrize(
    "total, risk, expect", [(100, 100, 18.92), (999, 1000, 28.89), (1e4, 1e3, 35.54), (100000, 1e12, 72.08), (10.0e9, 1.0e21, 135.2)]
)
def test_bits_for_total_risk(total, risk, expect):
    assert round(bits_for_total_risk(total, risk), 2) == expect


def test_bits_per_predefined_chars():
    assert bits_per_char(PredefinedChars(Chars.ALPHANUM)) == 5.954196310386875


def test_bits_per_custom_chars():
    assert bits_per_char(CustomChars('dingosky')) == 3.0


def test_bits_per_not_valid_chars():
    with pytest.raises(InvalidChars):
        bits_per_char('dingosky_dog')


@pytest.mark.parametrize("chars, len, expect", [(CustomChars('dingosky'), 14, 42), (PredefinedChars(Chars.SAFE_ASCII), 15, 97)])
def test_bits_for_len(chars, len, expect):
    assert bits_for_len(chars, len) == expect


@pytest.mark.parametrize("chars, bits, expect", [(CustomChars('dingosky'), 42, 14), (PredefinedChars(Chars.BASE32_HEX), 62, 13)])
def test_len_for_bits(chars, bits, expect):
    assert len_for_bits(chars, bits) == expect
