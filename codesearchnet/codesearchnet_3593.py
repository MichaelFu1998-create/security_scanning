def CALLDATALOAD(self, offset):
        """Get input data of current environment"""

        if issymbolic(offset):
            if solver.can_be_true(self._constraints, offset == self._used_calldata_size):
                self.constraints.add(offset == self._used_calldata_size)
            raise ConcretizeArgument(1, policy='SAMPLED')

        self._use_calldata(offset, 32)

        data_length = len(self.data)

        bytes = []
        for i in range(32):
            try:
                c = Operators.ITEBV(8, offset + i < data_length, self.data[offset + i], 0)
            except IndexError:
                # offset + i is concrete and outside data
                c = 0

            bytes.append(c)
        return Operators.CONCAT(256, *bytes)