def can_be_true(self, constraints, expression):
        """Check if two potentially symbolic values can be equal"""
        if isinstance(expression, bool):
            if not expression:
                return expression
            else:
                # if True check if constraints are feasible
                self._reset(constraints)
                return self._is_sat()
        assert isinstance(expression, Bool)

        with constraints as temp_cs:
            temp_cs.add(expression)
            self._reset(temp_cs.to_string(related_to=expression))
            return self._is_sat()