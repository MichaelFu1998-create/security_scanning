def show_condition_operators(self, condition):
        """ Show available operators for a given saved search condition """
        # dict keys of allowed operators for the current condition
        permitted_operators = self.savedsearch.conditions_operators.get(condition)
        # transform these into values
        permitted_operators_list = set(
            [self.savedsearch.operators.get(op) for op in permitted_operators]
        )
        return permitted_operators_list