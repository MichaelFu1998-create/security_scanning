def constrain(self, constraint):
        """Constrain state.

        :param manticore.core.smtlib.Bool constraint: Constraint to add
        """
        constraint = self.migrate_expression(constraint)
        self._constraints.add(constraint)