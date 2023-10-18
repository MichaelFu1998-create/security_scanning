def new_state(self):
        """Generates a state string to be used in authorizations."""
        try:
            self._state = self.state()
            log.debug("Generated new state %s.", self._state)
        except TypeError:
            self._state = self.state
            log.debug("Re-using previously supplied state %s.", self._state)
        return self._state