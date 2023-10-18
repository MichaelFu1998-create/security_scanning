def parse_operand(self, buf):
        """ Parses an operand from buf

            :param buf: a buffer
            :type buf: iterator/generator/string
        """
        buf = iter(buf)
        try:
            operand = 0
            for _ in range(self.operand_size):
                operand <<= 8
                operand |= next(buf)
            self._operand = operand
        except StopIteration:
            raise ParseError("Not enough data for decoding")