def _deserialize_uint(data, nbytes=32, padding=0, offset=0):
        """
        Read a `nbytes` bytes long big endian unsigned integer from `data` starting at `offset`

        :param data: sliceable buffer; symbolic buffer of Eth ABI encoded data
        :param nbytes: number of bytes to read starting from least significant byte
        :rtype: int or Expression
        """
        assert isinstance(data, (bytearray, Array))
        value = ABI._readBE(data, nbytes, padding=True, offset=offset)
        value = Operators.ZEXTEND(value, (nbytes + padding) * 8)
        return value