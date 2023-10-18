def _deserialize_int(data, nbytes=32, padding=0):
        """
        Read a `nbytes` bytes long big endian signed integer from `data` starting at `offset`

        :param data: sliceable buffer; symbolic buffer of Eth ABI encoded data
        :param nbytes: number of bytes to read starting from least significant byte
        :rtype: int or Expression
        """
        assert isinstance(data, (bytearray, Array))
        value = ABI._readBE(data, nbytes, padding=True)
        value = Operators.SEXTEND(value, nbytes * 8, (nbytes + padding) * 8)
        if not issymbolic(value):
            # sign bit on
            if value & (1 << (nbytes * 8 - 1)):
                value = -(((~value) + 1) & ((1 << (nbytes * 8)) - 1))
        return value