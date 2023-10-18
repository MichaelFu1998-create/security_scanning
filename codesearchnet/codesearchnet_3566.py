def _serialize_int(value, size=32, padding=0):
        """
        Translates a signed python integral or a BitVec into a 32 byte string, MSB first
        """
        if size <= 0 or size > 32:
            raise ValueError
        if not isinstance(value, (int, BitVec)):
            raise ValueError
        if issymbolic(value):
            buf = ArrayVariable(index_bits=256, index_max=32, value_bits=8, name='temp{}'.format(uuid.uuid1()))
            value = Operators.SEXTEND(value, value.size, size * 8)
            buf = ArrayProxy(buf.write_BE(padding, value, size))
        else:
            value = int(value)
            buf = bytearray()
            for _ in range(padding):
                buf.append(0)

            for position in reversed(range(size)):
                buf.append(Operators.EXTRACT(value, position * 8, 8))
        return buf