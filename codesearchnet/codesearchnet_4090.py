def steps(self):
        """Return a list of steps (statements that are not settings or comments)"""
        steps = []
        for statement in self.statements:
            if ((not statement.is_comment()) and
                (not statement.is_setting())):
                steps.append(statement)
        return steps