def solve_min(self, expr):
        """
        Solves a symbolic :class:`~manticore.core.smtlib.expression.Expression` into
        its minimum solution

        :param manticore.core.smtlib.Expression expr: Symbolic value to solve
        :return: Concrete value
        :rtype: list[int]
        """
        if isinstance(expr, int):
            return expr
        expr = self.migrate_expression(expr)
        return self._solver.min(self._constraints, expr)