def _serialize_uint(value, size=32, padding=0):
        """
        Translates a python integral or a BitVec into a 32 byte string, MSB first
        """
        if size <= 0 or size > 32:
            raise ValueError

        from .account import EVMAccount  # because of circular import
        if not isinstance(value, (int, BitVec, EVMAccount)):
            raise ValueError
        if issymbolic(value):
            # FIXME This temporary array variable should be obtained from a specific constraint store
            bytes = ArrayVariable(index_bits=256, index_max=32, value_bits=8, name='temp{}'.format(uuid.uuid1()))
            if value.size <= size * 8:
                value = Operators.ZEXTEND(value, size * 8)
            else:
                # automatically truncate, e.g. if they passed a BitVec(256) for an `address` argument (160 bits)
                value = Operators.EXTRACT(value, 0, size * 8)
            bytes = ArrayProxy(bytes.write_BE(padding, value, size))
        else:
            value = int(value)
            bytes = bytearray()
            for _ in range(padding):
                bytes.append(0)
            for position in reversed(range(size)):
                bytes.append(Operators.EXTRACT(value, position * 8, 8))
        assert len(bytes) == size + padding
        return bytes