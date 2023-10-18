def solve_one(self, expr, constrain=False):
        """
        Concretize a symbolic :class:`~manticore.core.smtlib.expression.Expression` into
        one solution.

        :param manticore.core.smtlib.Expression expr: Symbolic value to concretize
        :param bool constrain: If True, constrain expr to concretized value
        :return: Concrete value
        :rtype: int
        """
        expr = self.migrate_expression(expr)
        value = self._solver.get_value(self._constraints, expr)
        if constrain:
            self.constrain(expr == value)
        #Include forgiveness here
        if isinstance(value, bytearray):
            value = bytes(value)
        return value