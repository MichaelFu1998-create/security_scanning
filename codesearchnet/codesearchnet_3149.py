def _try_get_solutions(self, address, size, access, max_solutions=0x1000, force=False):
        """
        Try to solve for a symbolic address, checking permissions when reading/writing size bytes.

        :param Expression address: The address to solve for
        :param int size: How many bytes to check permissions for
        :param str access: 'r' or 'w'
        :param int max_solutions: Will raise if more solutions are found
        :param force: Whether to ignore permission failure
        :rtype: list
        """
        assert issymbolic(address)

        solutions = solver.get_all_values(self.constraints, address, maxcnt=max_solutions)

        crashing_condition = False
        for base in solutions:
            if not self.access_ok(slice(base, base + size), access, force):
                crashing_condition = Operators.OR(address == base, crashing_condition)

        if solver.can_be_true(self.constraints, crashing_condition):
            raise InvalidSymbolicMemoryAccess(address, access, size, crashing_condition)

        return solutions