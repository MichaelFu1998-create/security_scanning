def _getvalue(self, expression):
        """
        Ask the solver for one possible assignment for given expression using current set of constraints.
        The current set of expressions must be sat.

        NOTE: This is an internal method: it uses the current solver state (set of constraints!).
        """
        if not issymbolic(expression):
            return expression
        assert isinstance(expression, Variable)

        if isinstance(expression, Array):
            result = bytearray()
            for c in expression:
                expression_str = translate_to_smtlib(c)
                self._send('(get-value (%s))' % expression_str)
                response = self._recv()
                result.append(int('0x{:s}'.format(response.split(expression_str)[1][3:-2]), 16))
            return bytes(result)
        else:
            self._send('(get-value (%s))' % expression.name)
            ret = self._recv()
            assert ret.startswith('((') and ret.endswith('))'), ret

            if isinstance(expression, Bool):
                return {'true': True, 'false': False}[ret[2:-2].split(' ')[1]]
            elif isinstance(expression, BitVec):
                pattern, base = self._get_value_fmt
                m = pattern.match(ret)
                expr, value = m.group('expr'), m.group('value')
                return int(value, base)

        raise NotImplementedError("_getvalue only implemented for Bool and BitVec")