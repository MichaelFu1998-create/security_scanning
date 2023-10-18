def bytes(self):
        """ Encoded instruction """
        b = [bytes([self._opcode])]
        for offset in reversed(range(self.operand_size)):
            b.append(bytes([(self.operand >> offset * 8) & 0xff]))
        return b''.join(b)