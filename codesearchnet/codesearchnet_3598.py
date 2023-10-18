def MSTORE(self, address, value):
        """Save word to memory"""
        if istainted(self.pc):
            for taint in get_taints(self.pc):
                value = taint_with(value, taint)
        self._allocate(address, 32)
        self._store(address, value, 32)