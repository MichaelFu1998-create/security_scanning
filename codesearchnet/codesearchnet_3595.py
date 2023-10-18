def CODECOPY(self, mem_offset, code_offset, size):
        """Copy code running in current environment to memory"""

        self._allocate(mem_offset, size)
        GCOPY = 3             # cost to copy one 32 byte word
        copyfee = self.safe_mul(GCOPY, Operators.UDIV(self.safe_add(size, 31), 32))
        self._consume(copyfee)

        if issymbolic(size):
            max_size = solver.max(self.constraints, size)
        else:
            max_size = size

        for i in range(max_size):
            if issymbolic(i < size):
                default = Operators.ITEBV(8, i < size, 0, self._load(mem_offset + i, 1))  # Fixme. unnecessary memory read
            else:
                if i < size:
                    default = 0
                else:
                    default = self._load(mem_offset + i, 1)

            if issymbolic(code_offset):
                value = Operators.ITEBV(8, code_offset + i >= len(self.bytecode), default, self.bytecode[code_offset + i])
            else:
                if code_offset + i >= len(self.bytecode):
                    value = default
                else:
                    value = self.bytecode[code_offset + i]
            self._store(mem_offset + i, value)
        self._publish('did_evm_read_code', code_offset, size)