def _check_jmpdest(self):
        """
        If the previous instruction was a JUMP/JUMPI and the conditional was
        True, this checks that the current instruction must be a JUMPDEST.

        Here, if symbolic, the conditional `self._check_jumpdest` would be
        already constrained to a single concrete value.
        """
        should_check_jumpdest = self._check_jumpdest
        if issymbolic(should_check_jumpdest):
            should_check_jumpdest_solutions = solver.get_all_values(self.constraints, should_check_jumpdest)
            if len(should_check_jumpdest_solutions) != 1:
                raise EthereumError("Conditional not concretized at JMPDEST check")
            should_check_jumpdest = should_check_jumpdest_solutions[0]

        if should_check_jumpdest:
            self._check_jumpdest = False

            pc = self.pc.value if isinstance(self.pc, Constant) else self.pc

            if pc not in self._valid_jumpdests:
                raise InvalidOpcode()