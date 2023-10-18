def _should_run(self, iteration, max_iterations):
        ''' Return False if bot should quit '''
        if iteration == 0:
            # First frame always runs
            return True
        if max_iterations:
            if iteration < max_iterations:
                return True
        elif max_iterations is None:
            if self._dynamic:
                return True
            else:
                return False
            return True
        if not self._dynamic:
            return False

        return False