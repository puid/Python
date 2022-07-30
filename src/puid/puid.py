from math import ceil
from math import log2
from secrets import token_bytes

from puid import Chars
from puid.bits import muncher
from puid.chars import CustomChars
from puid.chars import PredefinedChars
from puid.chars_error import InvalidChars
from puid.encoder import encoder
from puid.entropy import bits_for_total_risk
from puid.puid_error import BitsError
from puid.puid_error import TotalRiskError


class Puid:
    def __init__(self, bits=None, total=None, risk=None, chars=None, entropy_source=None):

        base_bits = None
        if bits is None and total is None and risk is None:
            base_bits = 128
        elif bits is not None and (total is not None or risk is not None):
            raise BitsError("bits cannot be specified with total/risk")
        elif bits is not None and total is None and risk is None:
            if not isinstance(bits, int):
                raise BitsError("bits must be non-negative integer")
            if bits <= 0:
                raise BitsError("bits must be non-negative integer")
            base_bits = bits
        elif total is None and risk is not None:
            raise TotalRiskError("risk with no total")
        elif total is not None and risk is None:
            raise TotalRiskError("total with no risk")
        else:
            base_bits = bits_for_total_risk(total, risk)

        if chars is None:
            self.chars = PredefinedChars(Chars.SAFE64)
        elif isinstance(chars, Chars):
            self.chars = PredefinedChars(chars)
        elif isinstance(chars, str):
            self.chars = CustomChars(chars)
        else:
            raise InvalidChars('specified chars must be either Chars enum or string')

        n_chars = len(self.chars)
        n_bits_per_char = log2(n_chars)
        self.len = round(ceil(base_bits / n_bits_per_char))
        self.bits = self.len * n_bits_per_char
        entropy_fn = entropy_source or token_bytes
        self.entropy_source = f'{entropy_fn.__module__}.{entropy_fn.__name__}'

        self._chars_encoder = encoder(self.chars)
        self.bits_muncher = muncher(n_chars, self.len, entropy_fn)

        self.bits_per_char = n_bits_per_char

        chars_encoder = encoder(self.chars)
        self._encoded = lambda values: [chr(chars_encoder(value)) for value in values]

        self.ere = (n_bits_per_char * n_chars) / (8 * len(self.chars.value.encode('utf-8')))

    def __repr__(self):
        bits = round(self.bits, 2)
        bpc = round(self.bits_per_char, 2)
        return f'Puid: bits = {bits}, bits_per_char = {bpc}, chars = {self.chars}, len = {self.len}, '
        'ere = {self.ere}, entropy_source = {self.entropy_source}'

    def generate(self):
        values = self.bits_muncher()
        return "".join(self._encoded(values))
