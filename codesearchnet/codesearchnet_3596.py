def EXTCODECOPY(self, account, address, offset, size):
        """Copy an account's code to memory"""
        extbytecode = self.world.get_code(account)
        self._allocate(address + size)

        for i in range(size):
            if offset + i < len(extbytecode):
                self._store(address + i, extbytecode[offset + i])
            else:
                self._store(address + i, 0)