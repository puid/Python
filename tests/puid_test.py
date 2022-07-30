import pytest

from puid import Chars
from puid import Puid
from puid.chars_error import InvalidChars
from puid.chars_error import NonUniqueChars
from puid.puid_error import BitsError
from puid.puid_error import TotalRiskError


def fixed_bytes(hex_string):
    static_bytes = bytearray.fromhex(hex_string)
    offset = 0

    def get_bytes(n_bytes):
        nonlocal offset
        bytes = static_bytes[offset : offset + n_bytes]
        offset += n_bytes
        return bytes

    return get_bytes


def check_puid(id, bits, bpc, puid_len, ere, name):
    assert round(id.bits, 2) == bits
    assert round(id.bits_per_char, 2) == bpc
    assert round(id.ere, 2) == ere
    assert id.len == puid_len
    assert id.chars.name == name
    assert len(id.generate()) == puid_len


def test_default():
    rand_id = Puid()
    check_puid(rand_id, 132, 6, 22, 0.75, Chars.SAFE64.name)


def test_bits():
    rand_id = Puid(bits=48)
    check_puid(rand_id, 48, 6, 8, 0.75, Chars.SAFE64.name)


def test_total_risk():
    rand_id = Puid(total=250_000, risk=1e12)
    check_puid(rand_id, 78, 6, 13, 0.75, Chars.SAFE64.name)


def test_entropy_source():
    from random import getrandbits

    def prng_bytes(n):
        return bytearray(getrandbits(8) for _ in range(n))

    prng_id = Puid(entropy_source=prng_bytes)
    check_puid(prng_id, 132, 6, 22, 0.75, Chars.SAFE64.name)


def test_invalid_bits():
    with pytest.raises(BitsError):
        Puid(bits=-10)

    with pytest.raises(BitsError):
        Puid(bits=5.5)


def test_bits_and_total_risk():
    with pytest.raises(BitsError):
        Puid(bits=20, total=10000, risk=1e10)


def test_total_no_risk():
    with pytest.raises(TotalRiskError):
        Puid(total=10000)


def test_risk_no_total():
    with pytest.raises(TotalRiskError):
        Puid(risk=1e15)


def test_safe32_chars():
    rand_id = Puid(total=1e6, risk=1e15, chars=Chars.SAFE32)
    check_puid(rand_id, 90, 5, 18, 0.62, Chars.SAFE32.name)


def test_alpha_chars():
    rand_id = Puid(total=1e6, risk=1e15, chars=Chars.ALPHA)
    check_puid(rand_id, 91.21, 5.7, 16, 0.71, Chars.ALPHA.name)


def test_custom_chars():
    rand_id = Puid(chars='dingosky')
    check_puid(rand_id, 129, 3, 43, 0.38, "Custom")


def test_non_unique_chars():
    with pytest.raises(NonUniqueChars):
        Puid(chars='unique')


def test_invalid_chars():
    with pytest.raises(InvalidChars):
        Puid(chars='no space')

    with pytest.raises(InvalidChars):
        Puid(chars=['a', 'b', 'c'])


def test_char_count_pow_2():
    hex_bytes = fixed_bytes("99 b4 4f 80 c8 89")
    hex_id = Puid(bits=24, chars=Chars.HEX, entropy_source=hex_bytes)
    assert hex_id.generate() == "99b44f"
    assert hex_id.generate() == "80c889"


def test_3bit_custom():
    dingosky_bytes = fixed_bytes("c7 c9 00 2a bd 72")
    dingosky_id = Puid(bits=24, chars="dingosky", entropy_source=dingosky_bytes)
    assert dingosky_id.generate() == "kiyooodd"
    assert dingosky_id.generate() == "insgkskn"


def test_2bit_custom():
    dna_bytes = fixed_bytes("cb db 52 a2")
    dna_id = Puid(bits=16, chars="ATCG", entropy_source=dna_bytes)
    assert dna_id.generate() == "GACGGTCG"
    assert dna_id.generate() == "TTACCCAC"


def test_1bit_custom():
    tf_bytes = fixed_bytes("fb 04 2c b3")
    tf_id = Puid(bits=16, chars="FT", entropy_source=tf_bytes)
    assert tf_id.generate() == "TTTTTFTTFFFFFTFF"
    assert tf_id.generate() == "FFTFTTFFTFTTFFTT"


def test_hex_with_carry():
    hex_bytes = fixed_bytes("c7 c9 00 2a bd")
    hex_id = Puid(bits=12, chars=Chars.HEX_UPPER, entropy_source=hex_bytes)
    assert hex_id.generate() == "C7C"
    assert hex_id.generate() == "900"
    assert hex_id.generate() == "2AB"


def test_3bit_with_carry():
    #    C    7    C    9    0    0    2    A    B    D    7    2
    # 1100 0111 1100 1001 0000 0000 0010 1010 1011 1101 0111 0010
    #
    #  110 001 111 100 100 100 000 000 001 010 101 011 110 101 110 010
    #  |-| |-| |-| |-| |-| |-| |-| |-| |-| |-| |-| |-| |-| |-| |-| |-|
    #   k   i   y   o   o   o   d   d   i   n   s   g   k   s   k   n

    dingosky_bytes = fixed_bytes("c7 c9 00 2a bd 72")
    dingosky_id = Puid(bits=9, chars="dingosky", entropy_source=dingosky_bytes)
    assert dingosky_id.generate() == "kiy"
    assert dingosky_id.generate() == "ooo"
    assert dingosky_id.generate() == "ddi"
    assert dingosky_id.generate() == "nsg"
    assert dingosky_id.generate() == "ksk"


def test_3bit_unicode_with_carry():
    dingosky_bytes = fixed_bytes("c7 c9 00 2a bd 72")
    dingosky_id = Puid(bits=9, chars="dîngøsky", entropy_source=dingosky_bytes)
    assert dingosky_id.generate() == "kîy"
    assert dingosky_id.generate() == "øøø"
    assert dingosky_id.generate() == "ddî"
    assert dingosky_id.generate() == "nsg"
    assert dingosky_id.generate() == "ksk"


def test_5bit_with_carry():
    #    D    2    E    3    E    9    D    A    1    9    0    3    B    7    3    C
    # 1101 0010 1110 0011 1110 1001 1101 1010 0001 1001 0000 0011 1011 0111 0011 1100
    #
    # 11010 01011 10001 11110 10011 10110 10000 11001 00000 01110 11011 10011 1100
    # |---| |---| |---| |---| |---| |---| |---| |---| |---| |---| |---| |---|
    #   26    11    17    30    19    22    16    25     0    14    27    19
    #    M     h     r     R     B     G     q     L     2     n     N     B

    safe32_bytes = fixed_bytes("d2 e3 e9 da 19 03 b7 3c")
    safe32_id = Puid(bits=20, chars=Chars.SAFE32, entropy_source=safe32_bytes)
    assert safe32_id.generate() == "MhrR"
    assert safe32_id.generate() == "BGqL"
    assert safe32_id.generate() == "2nNB"


def test_5_plus_bit():
    # shifts: [ [ 26, 5 ], [ 31, 3 ] ]
    #
    #    5    3    c    8    8    d    e    6    3    e    2    6    a    0
    # 0101 0011 1100 1000 1000 1101 1110 0110 0011 1110 0010 0110 1010 0000
    #
    # 01010 01111 00100 01000 110 111 10011 00011 111 00010 01101 01000 00
    # |---| |---| |---| |---| xxx xxx |---| |---| xxx |---| |---| |---|
    #   10    15     4     8   27  30   19     3   28    2    13     8
    #    k     p     e     i             t     d         c     n     i
    alpha_lower_bytes = fixed_bytes("53 c8 8d e6 3e 26 a0")
    alpha_lower_id = Puid(bits=14, chars=Chars.ALPHA_LOWER, entropy_source=alpha_lower_bytes)
    assert alpha_lower_id.generate() == "kpe"
    assert alpha_lower_id.generate() == "itd"
    assert alpha_lower_id.generate() == "cni"


def test_6_plus_bit():
    #
    # shifts: [ [62, 6] ]
    #
    #    D    2    E    3    E    9    F    A    1    9    0    0
    # 1101 0010 1110 0011 1110 1001 1111 1010 0001 1001 0000 0000
    #
    # 110100 101110 001111 101001 111110 100001 100100 000000
    # |----| |----| |----| |----| xxxxxx |----| |----|
    #   52     46     15     41     62     33     36
    #    q      k      F      f             X      a
    #

    alphanum_bytes = fixed_bytes("d2 e3 e9 fa 19 00")
    alphanum_id = Puid(bits=17, chars=Chars.ALPHANUM, entropy_source=alphanum_bytes)
    assert alphanum_id.generate() == "qkF"
    assert alphanum_id.generate() == "fXa"


def test_base32():
    base32_bytes = fixed_bytes("d2 e3 e9 da 19 12 ce")
    base32_id = Puid(bits=25, chars=Chars.BASE32, entropy_source=base32_bytes)
    assert base32_id.generate() == "UFLYN"
    assert base32_id.generate() == "QKT4F"


def test_base32_hex():
    base32_hex_bytes = fixed_bytes("d2 e3 e9 da 19 12 ce 28")
    base32_hex_id = Puid(bits=30, chars=Chars.BASE32_HEX, entropy_source=base32_hex_bytes)
    assert base32_hex_id.generate() == "qbhujm"
    assert base32_hex_id.generate() == "gp2b72"


def test_base32_hex_upper():
    base32_hex_upper_bytes = fixed_bytes("d2 e3 e9 da 19 12 ce 28")
    base32_hex_upper_id = Puid(bits=20, chars=Chars.BASE32_HEX_UPPER, entropy_source=base32_hex_upper_bytes)
    assert base32_hex_upper_id.generate() == "QBHU"
    assert base32_hex_upper_id.generate() == "JMGP"
    assert base32_hex_upper_id.generate() == "2B72"


def test_alpha_upper():
    alpha_upper_id = Puid(bits=48, chars=Chars.ALPHA_UPPER)
    check_puid(alpha_upper_id, 51.7, 4.7, 11, 0.59, Chars.ALPHA_UPPER.name)


def test_safe_ascii():
    safe_ascii_id = Puid(bits=52, chars=Chars.SAFE_ASCII)
    check_puid(safe_ascii_id, 58.43, 6.49, 9, 0.81, Chars.SAFE_ASCII.name)


def test_256_chars():
    single_byte = Chars.SAFE64.value

    double_start = 256
    double_byte = "".join([chr(n + double_start) for n in range(128)])

    triple_start = 19904
    triple_byte = "".join([chr(n + triple_start) for n in range(64)])

    chars = single_byte + double_byte + triple_byte
    id = Puid(chars=chars)

    assert len(id.generate()) == id.len
    assert id.bits_per_char == 8
    assert id.ere == 0.5


def test_repr():
    rand_id = Puid()
    assert isinstance(rand_id.__repr__(), str)
