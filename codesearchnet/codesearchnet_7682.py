def unpack(word):
        r"""
        >>> PackedAttributes.unpack(0)
        0
        >>> PackedAttributes.unpack('\x00\x00\x00\x01')
        1
        >>> PackedAttributes.unpack('abcd')
        1633837924
        """
        if not isinstance(word, str):
            return word
        val, = struct.unpack('!I', word.encode('ascii'))
        return val