def _set_state(self, state, force=True):
        """
        Setting force to True allows for changing a state after it
        COMPLETED. This would otherwise be invalid.
        """
        self._setstate(state, True)
        self.last_state_change = time.time()