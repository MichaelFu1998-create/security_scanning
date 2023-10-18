def solve_buffer(self, addr, nbytes, constrain=False):
        """
        Reads `nbytes` of symbolic data from a buffer in memory at `addr` and attempts to
        concretize it

        :param int address: Address of buffer to concretize
        :param int nbytes: Size of buffer to concretize
        :param bool constrain: If True, constrain the buffer to the concretized value
        :return: Concrete contents of buffer
        :rtype: list[int]
        """
        buffer = self.cpu.read_bytes(addr, nbytes)
        result = []
        with self._constraints as temp_cs:
            cs_to_use = self.constraints if constrain else temp_cs
            for c in buffer:
                result.append(self._solver.get_value(cs_to_use, c))
                cs_to_use.add(c == result[-1])
        return result