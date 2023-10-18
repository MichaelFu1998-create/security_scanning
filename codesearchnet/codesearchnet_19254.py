def initial_closure(self):
        """Computes the initial closure using the START_foo production."""
        first_rule = DottedRule(self.start, 0, END_OF_INPUT)
        return self.closure([first_rule])