def solve_max(self, expr):
        """
        Solves a symbolic :class:`~manticore.core.smtlib.expression.Expression` into
        its maximum solution

        :param manticore.core.smtlib.Expression expr: Symbolic value to solve
        :return: Concrete value
        :rtype: list[int]
        """
        if isinstance(expr, int):
            return expr
        expr = self.migrate_expression(expr)
        return self._solver.max(self._constraints, expr)