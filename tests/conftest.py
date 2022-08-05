import os
from collections import namedtuple

import pytest

from puid import Chars
from puid import Puid


class Util:
    Params = namedtuple('Params', 'bin_file mod_name total risk chars ids_count')

    @staticmethod
    def fixed_bytes_string(hex_string):
        return Util.fixed_bytes(bytearray.fromhex(hex_string))

    @staticmethod
    def fixed_bytes(static_bytes):
        bytes = static_bytes
        offset = 0

        def get_bytes(n_bytes):
            nonlocal offset
            offset_bytes = bytes[offset : offset + n_bytes]
            offset += n_bytes
            return offset_bytes

        return get_bytes

    @staticmethod
    def file_bytes(bin_file):
        with open(bin_file, 'rb') as file:
            return Util.fixed_bytes(bytearray(file.read()))

    @staticmethod
    def data_dir(data_name):
        return os.path.join(os.getcwd(), 'tests', 'data', data_name)

    @staticmethod
    def data_path(data_name, file_name):
        return os.path.join(Util.data_dir(data_name), file_name)

    @staticmethod
    def params(data_name):
        params_path = os.path.join(Util.data_path(data_name, 'params'))
        with open(params_path, 'r') as file:

            def next_param():
                return file.readline().strip()

            bin_file = Util.data_path('', next_param())
            test_name = next_param()
            total = int(next_param())
            risk = float(next_param())

            chars = Util.chars_param(next_param())
            count = int(next_param())

            return Util.Params(bin_file, test_name, total, risk, chars, count)

    @staticmethod
    def chars_param(param):
        chars_type, chars_def = param.split(':')
        if chars_type == 'predefined':
            return Util.predefined(chars_def)
        elif chars_type == 'custom':
            return chars_def
        else:
            raise ValueError('params file has invalid chars def:', param)

    @staticmethod
    def predefined(name):
        if name == 'alphanum':
            return Chars.ALPHANUM
        return None

    @staticmethod
    def rand_id_mod(dir_name):
        params = Util.params(dir_name)
        rand_bytes = Util.file_bytes(params.bin_file)
        return Puid(total=params.total, risk=params.risk, chars=params.chars, entropy_source=rand_bytes)

    @staticmethod
    def test_data(data_name):
        rand_id = Util.rand_id_mod(data_name)
        ids_file = Util.data_path(data_name, 'ids')

        with open(ids_file) as ids:
            for id in ids:
                assert rand_id.generate() == id.strip()


@pytest.fixture
def util():
    return Util
