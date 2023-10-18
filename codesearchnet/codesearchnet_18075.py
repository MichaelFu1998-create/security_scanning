def push_update(self, params, values):
        """
        Perform a parameter update and keep track of the change on the state.
        Same call structure as :func:`peri.states.States.update`
        """
        curr = self.get_values(params)
        self.stack.append((params, curr))
        self.update(params, values)