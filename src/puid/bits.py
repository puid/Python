from math import ceil
from math import floor
from math import log2

#  Create array of minimum bits required to determine if a value is less than n_chars
#  Array elements are of the form (n, bits): For values less than n, bits bits are required
#
#  As example, the bits shifts array for the 36 AlphaNumLower characters is:
#    (36, 6), (39, 5), (47, 3), (63, 2)
#
#  Each value slice uses 6 bits of entropy. In bits, 36 is 100100.
#  Now suppose we slice the value 50. In bits, 50 is 110010.
#
#  Only two bits are necessary to determine 100100 < 110010
#


def bit_shifts(n_chars):
    n_bits_per_char = ceil(log2(n_chars))

    base_shift = (n_chars, n_bits_per_char)

    if log2(n_chars).is_integer():
        return [base_shift]

    def is_bit_zero(bit):
        return n_chars & (1 << (bit - 1)) == 0

    def pow2(bit):
        return round(pow(2, bit))

    def shift(bit):
        return (n_chars | pow2(bit) - 1, n_bits_per_char - bit + 1)

    return [base_shift] + [shift(bit) for bit in range(2, n_bits_per_char) if is_bit_zero(bit)]


def fill_entropy(entropy_offset, entropy_bytes, entropy_fn):
    n_bytes = len(entropy_bytes)
    n_bits = 8 * n_bytes

    if entropy_offset == n_bits:
        # no carry
        entropy_bytes[0:n_bytes] = entropy_fn(n_bytes)
    else:
        offset_byte_num = floor(entropy_offset / 8)

        # Move unused bytes to the left
        entropy_bytes[0 : n_bytes - offset_byte_num] = entropy_bytes[offset_byte_num:n_bytes]

        # Fill right bytes with new random values
        entropy_bytes[n_bytes - offset_byte_num : n_bytes] = entropy_fn(offset_byte_num)

    return entropy_offset % 8


def value_at(l_offset, n_bits, bytes):
    l_byte_ndx = floor(l_offset / 8)
    l_byte = bytes[l_byte_ndx]

    l_bit_num = l_offset % 8

    if l_bit_num + n_bits <= 8:
        return ((l_byte << l_bit_num) & 0xFF) >> (8 - n_bits)

    r_byte = bytes[l_byte_ndx + 1]
    r_bit_num = l_bit_num + n_bits - 8

    l_value = ((l_byte << l_bit_num) & 0xFF) >> (l_bit_num - r_bit_num)
    r_value = r_byte >> (8 - r_bit_num)

    return l_value + r_value


def muncher(n_chars, puid_len, entropy_fn):
    n_bits_per_char = ceil(log2(n_chars))
    n_bits_per_puid = n_bits_per_char * puid_len
    n_bytes_per_puid = ceil(n_bits_per_puid / 8)

    buffer_len = n_bytes_per_puid + 1
    n_entropy_bits = 8 * buffer_len
    entropy_offset = n_entropy_bits
    entropy_bytes = bytearray(buffer_len)

    def pow2(bit):
        return round(pow(2, bit))

    def is_pow2(n):
        return pow2(round(log2(n))) == n

    counter = list(range(puid_len))

    def sliced_value():
        nonlocal entropy_offset
        if n_entropy_bits < entropy_offset + n_bits_per_char:
            entropy_offset = fill_entropy(entropy_offset, entropy_bytes, entropy_fn)
        return value_at(entropy_offset, n_bits_per_char, entropy_bytes)

    if is_pow2(n_chars):
        #  When chars count is a power of 2, sliced bits always yield a valid value
        def bits_muncher():
            def slice_value():
                nonlocal entropy_offset
                value = sliced_value()
                entropy_offset += n_bits_per_char
                return value

            puid = [slice_value() for _ in counter]
            return puid

        return bits_muncher

    shifts = bit_shifts(n_chars)

    def accept_value(value):
        # Value is valid if it is less than the number of characters
        if value < n_chars:
            return (True, n_bits_per_char)

        # For invalid value, shift the minimal bits necessary to determine validity
        return (False, next((shift for shift in shifts if value < shift[0]), shifts[0])[1])

    def slice_value():
        nonlocal entropy_offset
        value = sliced_value()
        accept, shift = accept_value(value)
        # Returned shift is the minimal bits necessary to determine if slice value is valid
        entropy_offset += shift

        if accept:
            return value

        # If value not acceptable, slice another
        return slice_value()

    def bits_muncher():
        puid = [slice_value() for _ in counter]
        return puid

    return bits_muncher
