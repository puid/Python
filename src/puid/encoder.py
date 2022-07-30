from puid.chars import Chars
from puid.encoders.alpha import alpha
from puid.encoders.alpha import alpha_lower
from puid.encoders.alpha import alpha_upper
from puid.encoders.alphanum import alphanum
from puid.encoders.alphanum import alphanum_lower
from puid.encoders.alphanum import alphanum_upper
from puid.encoders.base32 import base32
from puid.encoders.base32 import base32_hex
from puid.encoders.base32 import base32_hex_upper
from puid.encoders.custom import custom
from puid.encoders.decimal import decimal
from puid.encoders.hex import hex_lower
from puid.encoders.hex import hex_upper
from puid.encoders.safe32 import safe32
from puid.encoders.safe64 import safe64
from puid.encoders.safe_ascii import safe_ascii
from puid.encoders.symbol import symbol


def encoder(chars: Chars):
    if chars.name == Chars.ALPHA.name:
        return alpha()

    if chars.name == Chars.ALPHA_LOWER.name:
        return alpha_lower()

    if chars.name == Chars.ALPHA_UPPER.name:
        return alpha_upper()

    if chars.name == Chars.ALPHANUM.name:
        return alphanum()

    if chars.name == Chars.ALPHANUM_LOWER.name:
        return alphanum_lower()

    if chars.name == Chars.ALPHANUM_UPPER.name:
        return alphanum_upper()

    if chars.name == Chars.BASE32.name:
        return base32()

    if chars.name == Chars.BASE32_HEX.name:
        return base32_hex()

    if chars.name == Chars.BASE32_HEX_UPPER.name:
        return base32_hex_upper()

    if chars.name == Chars.DECIMAL.name:
        return decimal()

    if chars.name == Chars.HEX.name:
        return hex_lower()

    if chars.name == Chars.HEX_UPPER.name:
        return hex_upper()

    if chars.name == Chars.SAFE32.name:
        return safe32()

    if chars.name == Chars.SAFE64.name:
        return safe64()

    if chars.name == Chars.SAFE_ASCII.name:
        return safe_ascii()

    if chars.name == Chars.SYMBOL.name:
        return symbol()

    return custom(chars)
