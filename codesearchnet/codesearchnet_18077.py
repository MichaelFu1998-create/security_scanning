def temp_update(self, params, values):
        """
        Context manager to temporarily perform a parameter update (by using the
        stack structure). To use:

            with state.temp_update(params, values):
                # measure the cost or something
                state.error
        """
        self.push_update(params, values)
        yield
        self.pop_update()