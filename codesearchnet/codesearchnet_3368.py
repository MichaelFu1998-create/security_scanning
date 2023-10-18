def get_all_values(self, constraints, expression, maxcnt=None, silent=False):
        """Returns a list with all the possible values for the symbol x"""
        if not isinstance(expression, Expression):
            return [expression]
        assert isinstance(constraints, ConstraintSet)
        assert isinstance(expression, Expression)
        expression = simplify(expression)
        if maxcnt is None:
            maxcnt = consts.maxsolutions

        with constraints as temp_cs:
            if isinstance(expression, Bool):
                var = temp_cs.new_bool()
            elif isinstance(expression, BitVec):
                var = temp_cs.new_bitvec(expression.size)
            elif isinstance(expression, Array):
                var = temp_cs.new_array(index_max=expression.index_max, value_bits=expression.value_bits, taint=expression.taint).array
            else:
                raise NotImplementedError(f"get_all_values only implemented for {type(expression)} expression type.")

            temp_cs.add(var == expression)
            self._reset(temp_cs.to_string(related_to=var))

            result = []

            while self._is_sat():
                value = self._getvalue(var)
                result.append(value)
                self._assert(var != value)

                if len(result) >= maxcnt:
                    if silent:
                        # do not throw an exception if set to silent
                        # Default is not silent, assume user knows
                        # what they are doing and will check the size
                        # of returned vals list (previous smtlib behavior)
                        break
                    else:
                        raise TooManySolutions(result)

            return result