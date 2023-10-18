def symbolicate_buffer(self, data, label='INPUT', wildcard='+', string=False, taint=frozenset()):
        """Mark parts of a buffer as symbolic (demarked by the wildcard byte)

        :param str data: The string to symbolicate. If no wildcard bytes are provided,
                this is the identity function on the first argument.
        :param str label: The label to assign to the value
        :param str wildcard: The byte that is considered a wildcard
        :param bool string: Ensure bytes returned can not be NULL
        :param taint: Taint identifier of the symbolicated data
        :type taint: tuple or frozenset

        :return: If data does not contain any wildcard bytes, data itself. Otherwise,
            a list of values derived from data. Non-wildcard bytes are kept as
            is, wildcard bytes are replaced by Expression objects.
        """
        if wildcard in data:
            size = len(data)
            symb = self._constraints.new_array(name=label, index_max=size, taint=taint, avoid_collisions=True)
            self._input_symbols.append(symb)

            tmp = []
            for i in range(size):
                if data[i] == wildcard:
                    tmp.append(symb[i])
                else:
                    tmp.append(data[i])

            data = tmp

        if string:
            for b in data:
                if issymbolic(b):
                    self._constraints.add(b != 0)
                else:
                    assert b != 0
        return data