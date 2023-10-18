def _BYTES_TO_BITS():
    """Generate a table to convert a whole byte to binary.
    This code was taken from the Python Cookbook, 2nd edition - O'Reilly."""
    the_table = 256*[None]
    bits_per_byte = list(range(7, -1, -1))
    for n in range(256):
        l = n
        bits = 8*[None]
        for i in bits_per_byte:
            bits[i] = '01'[n & 1]
            n >>= 1
        the_table[l] = ''.join(bits)
    return the_table