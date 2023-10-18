def optimize(self, constraints: ConstraintSet, x: BitVec, goal: str, M=10000):
        """
        Iteratively finds the maximum or minimum value for the operation
        (Normally Operators.UGT or Operators.ULT)

        :param constraints: constraints to take into account
        :param x: a symbol or expression
        :param goal: goal to achieve, either 'maximize' or 'minimize'
        :param M: maximum number of iterations allowed
        """
        assert goal in ('maximize', 'minimize')
        assert isinstance(x, BitVec)
        operation = {'maximize': Operators.UGE, 'minimize': Operators.ULE}[goal]

        with constraints as temp_cs:
            X = temp_cs.new_bitvec(x.size)
            temp_cs.add(X == x)
            aux = temp_cs.new_bitvec(X.size, name='optimized_')
            self._reset(temp_cs.to_string(related_to=X))
            self._send(aux.declaration)

            if getattr(self, f'support_{goal}'):
                self._push()
                try:
                    self._assert(operation(X, aux))
                    self._send('(%s %s)' % (goal, aux.name))
                    self._send('(check-sat)')
                    _status = self._recv()
                    if _status not in ('sat', 'unsat', 'unknown'):
                        # Minimize (or Maximize) sometimes prints the objective before the status
                        # This will be a line like NAME |-> VALUE
                        maybe_sat = self._recv()
                        if maybe_sat == 'sat':
                            m = RE_MIN_MAX_OBJECTIVE_EXPR_VALUE.match(_status)
                            expr, value = m.group('expr'), m.group('value')
                            assert expr == aux.name
                            return int(value)
                    elif _status == 'sat':
                        ret = self._recv()
                        if not (ret.startswith('(') and ret.endswith(')')):
                            raise SolverError('bad output on max, z3 may have been killed')

                        m = RE_OBJECTIVES_EXPR_VALUE.match(ret)
                        expr, value = m.group('expr'), m.group('value')
                        assert expr == aux.name
                        return int(value)
                finally:
                    self._pop()
                    self._reset(temp_cs)
                    self._send(aux.declaration)

            operation = {'maximize': Operators.UGT, 'minimize': Operators.ULT}[goal]
            self._assert(aux == X)
            last_value = None
            i = 0
            while self._is_sat():
                last_value = self._getvalue(aux)
                self._assert(operation(aux, last_value))
                i = i + 1
                if i > M:
                    raise SolverError("Optimizing error, maximum number of iterations was reached")
            if last_value is not None:
                return last_value
            raise SolverError("Optimizing error, unsat or unknown core")