def _update_state(self, vals):
        """
        Takes as input a list or tuple of two elements. First the
        value returned by incrementing by 'stepsize' followed by the
        value returned after a 'stepsize' decrement.
        """
        self._steps_complete += 1
        if self._steps_complete == self.max_steps:
            self._termination_info = (False, self._best_val, self._arg)
            return StopIteration

        arg_inc, arg_dec = vals
        best_val = min(arg_inc, arg_dec, self._best_val)
        if best_val == self._best_val:
            self._termination_info = (True, best_val, self._arg)
            return StopIteration

        self._arg += self.stepsize if (arg_dec > arg_inc) else -self.stepsize
        self._best_val= best_val
        return [{self.key:self._arg+self.stepsize},
                {self.key:self._arg-self.stepsize}]