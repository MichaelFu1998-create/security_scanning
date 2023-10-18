def check_condition(self, condition):
        """Helper that returns True if condition is satisfied/doesn't exist.
        """
        if not condition:
            return True
        for c in condition.conditions:
            key, value, operator = c
            if not operator(self.answers[key], value):
                return False
        return True