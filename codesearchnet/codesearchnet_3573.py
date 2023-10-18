def read_code(self, address, size=1):
        """
        Read size byte from bytecode.
        If less than size bytes are available result will be pad with \x00
        """
        assert address < len(self.bytecode)
        value = self.bytecode[address:address + size]
        if len(value) < size:
            value += '\x00' * (size - len(value))  # pad with null (spec)
        return value