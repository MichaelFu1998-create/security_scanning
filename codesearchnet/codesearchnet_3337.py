def new_symbolic_buffer(self, nbytes, **options):
        """Create and return a symbolic buffer of length `nbytes`. The buffer is
        not written into State's memory; write it to the state's memory to
        introduce it into the program state.

        :param int nbytes: Length of the new buffer
        :param str label: (keyword arg only) The label to assign to the buffer
        :param bool cstring: (keyword arg only) Whether or not to enforce that the buffer is a cstring
                 (i.e. no NULL bytes, except for the last byte). (bool)
        :param taint: Taint identifier of the new buffer
        :type taint: tuple or frozenset

        :return: :class:`~manticore.core.smtlib.expression.Expression` representing the buffer.
        """
        label = options.get('label')
        avoid_collisions = False
        if label is None:
            label = 'buffer'
            avoid_collisions = True
        taint = options.get('taint', frozenset())
        expr = self._constraints.new_array(name=label, index_max=nbytes, value_bits=8, taint=taint, avoid_collisions=avoid_collisions)
        self._input_symbols.append(expr)

        if options.get('cstring', False):
            for i in range(nbytes - 1):
                self._constraints.add(expr[i] != 0)

        return expr