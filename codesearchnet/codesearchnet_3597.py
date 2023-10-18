def MLOAD(self, address):
        """Load word from memory"""
        self._allocate(address, 32)
        value = self._load(address, 32)
        return value