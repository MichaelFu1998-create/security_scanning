def solve_minmax(self, expr):
        """
        Solves a symbolic :class:`~manticore.core.smtlib.expression.Expression` into
        its minimum and maximun solution. Only defined for bitvects.

        :param manticore.core.smtlib.Expression expr: Symbolic value to solve
        :return: Concrete value
        :rtype: list[int]
        """
        if isinstance(expr, int):
            return expr
        expr = self.migrate_expression(expr)
        return self._solver.minmax(self._constraints, expr)