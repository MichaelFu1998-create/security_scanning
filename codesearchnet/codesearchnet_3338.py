def new_symbolic_value(self, nbits, label=None, taint=frozenset()):
        """Create and return a symbolic value that is `nbits` bits wide. Assign
        the value to a register or write it into the address space to introduce
        it into the program state.

        :param int nbits: The bitwidth of the value returned
        :param str label: The label to assign to the value
        :param taint: Taint identifier of this value
        :type taint: tuple or frozenset
        :return: :class:`~manticore.core.smtlib.expression.Expression` representing the value
        """
        assert nbits in (1, 4, 8, 16, 32, 64, 128, 256)
        avoid_collisions = False
        if label is None:
            label = 'val'
            avoid_collisions = True

        expr = self._constraints.new_bitvec(nbits, name=label, taint=taint, avoid_collisions=avoid_collisions)
        self._input_symbols.append(expr)
        return expr