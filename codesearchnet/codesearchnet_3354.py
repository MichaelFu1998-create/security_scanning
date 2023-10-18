def must_be_true(self, constraints, expression) -> bool:
        """Check if expression is True and that it can not be False with current constraints"""
        solutions = self.get_all_values(constraints, expression, maxcnt=2, silent=True)
        return solutions == [True]