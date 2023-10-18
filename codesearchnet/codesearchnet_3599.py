def MSTORE8(self, address, value):
        """Save byte to memory"""
        if istainted(self.pc):
            for taint in get_taints(self.pc):
                value = taint_with(value, taint)
        self._allocate(address, 1)
        self._store(address, Operators.EXTRACT(value, 0, 8), 1)