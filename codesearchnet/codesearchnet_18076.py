def pop_update(self):
        """
        Pop the last update from the stack push by
        :func:`peri.states.States.push_update` by undoing the chnage last
        performed.
        """
        params, values = self.stack.pop()
        self.update(params, values)