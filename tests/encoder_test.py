from puid import Chars
from puid.encoder import encoder


def encoder_chars(chars):
    chars_encoder = encoder(chars)
    encoded = "".join([chr(chars_encoder(code)) for code in range(len(chars))])
    assert encoded == chars.value


def test_encoders():
    encoder_chars(Chars.ALPHA)
    encoder_chars(Chars.ALPHA_LOWER)
    encoder_chars(Chars.ALPHA_UPPER)
    encoder_chars(Chars.ALPHANUM)
    encoder_chars(Chars.ALPHANUM_LOWER)
    encoder_chars(Chars.ALPHANUM_UPPER)
    encoder_chars(Chars.BASE32)
    encoder_chars(Chars.BASE32_HEX)
    encoder_chars(Chars.BASE32_HEX_UPPER)
    encoder_chars(Chars.DECIMAL)
    encoder_chars(Chars.HEX)
    encoder_chars(Chars.HEX_UPPER)
    encoder_chars(Chars.SAFE_ASCII)
    encoder_chars(Chars.SAFE32)
    encoder_chars(Chars.SAFE64)
    encoder_chars(Chars.SYMBOL)
