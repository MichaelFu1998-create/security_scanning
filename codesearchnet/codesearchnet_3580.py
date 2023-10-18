def _store(self, offset, value, size=1):
        """Stores value in memory as a big endian"""
        self.memory.write_BE(offset, value, size)
        for i in range(size):
            self._publish('did_evm_write_memory', offset + i, Operators.EXTRACT(value, (size - i - 1) * 8, 8))