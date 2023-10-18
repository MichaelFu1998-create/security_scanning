def get_value(self, constraints, expression):
        """
        Ask the solver for one possible result of given expression using given set of constraints.
        """
        if not issymbolic(expression):
            return expression
        assert isinstance(expression, (Bool, BitVec, Array))
        with constraints as temp_cs:
            if isinstance(expression, Bool):
                var = temp_cs.new_bool()
            elif isinstance(expression, BitVec):
                var = temp_cs.new_bitvec(expression.size)
            elif isinstance(expression, Array):
                var = []
                result = []
                for i in range(expression.index_max):
                    subvar = temp_cs.new_bitvec(expression.value_bits)
                    var.append(subvar)
                    temp_cs.add(subvar == simplify(expression[i]))

                self._reset(temp_cs)
                if not self._is_sat():
                    raise SolverError('Model is not available')

                for i in range(expression.index_max):
                    self._send('(get-value (%s))' % var[i].name)
                    ret = self._recv()
                    assert ret.startswith('((') and ret.endswith('))')
                    pattern, base = self._get_value_fmt
                    m = pattern.match(ret)
                    expr, value = m.group('expr'), m.group('value')
                    result.append(int(value, base))
                return bytes(result)

            temp_cs.add(var == expression)

            self._reset(temp_cs)

        if not self._is_sat():
            raise SolverError('Model is not available')

        self._send('(get-value (%s))' % var.name)
        ret = self._recv()
        if not (ret.startswith('((') and ret.endswith('))')):
            raise SolverError('SMTLIB error parsing response: %s' % ret)

        if isinstance(expression, Bool):
            return {'true': True, 'false': False}[ret[2:-2].split(' ')[1]]
        if isinstance(expression, BitVec):
            pattern, base = self._get_value_fmt
            m = pattern.match(ret)
            expr, value = m.group('expr'), m.group('value')
            return int(value, base)
        raise NotImplementedError("get_value only implemented for Bool and BitVec")