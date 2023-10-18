def CALLDATACOPY(self, mem_offset, data_offset, size):
        """Copy input data in current environment to memory"""

        if issymbolic(size):
            if solver.can_be_true(self._constraints, size <= len(self.data) + 32):
                self.constraints.add(size <= len(self.data) + 32)
            raise ConcretizeArgument(3, policy='SAMPLED')

        if issymbolic(data_offset):
            if solver.can_be_true(self._constraints, data_offset == self._used_calldata_size):
                self.constraints.add(data_offset == self._used_calldata_size)
            raise ConcretizeArgument(2, policy='SAMPLED')

        #account for calldata usage
        self._use_calldata(data_offset, size)
        self._allocate(mem_offset, size)
        for i in range(size):
            try:
                c = Operators.ITEBV(8, data_offset + i < len(self.data), Operators.ORD(self.data[data_offset + i]), 0)
            except IndexError:
                # data_offset + i is concrete and outside data
                c = 0
            self._store(mem_offset + i, c)