def solve_n(self, expr, nsolves):
        """
        Concretize a symbolic :class:`~manticore.core.smtlib.expression.Expression` into
        `nsolves` solutions.

        :param manticore.core.smtlib.Expression expr: Symbolic value to concretize
        :return: Concrete value
        :rtype: list[int]
        """
        expr = self.migrate_expression(expr)
        return self._solver.get_all_values(self._constraints, expr, nsolves, silent=True)