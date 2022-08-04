import pytest


class Util:
    @staticmethod
    def fixed_bytes(hex_string):
        static_bytes = bytearray.fromhex(hex_string)
        offset = 0

        def get_bytes(n_bytes):
            nonlocal offset
            bytes = static_bytes[offset : offset + n_bytes]
            offset += n_bytes
            return bytes

        return get_bytes


@pytest.fixture
def util():
    return Util
