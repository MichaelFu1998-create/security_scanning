def _state_changed(self, state):
        """Called when the power state changes."""
        logger.debug('Adapter state change: {0}'.format(state))
        # Handle when powered on.
        if state == 5:
            self._powered_off.clear()
            self._powered_on.set()
        # Handle when powered off.
        elif state == 4:
            self._powered_on.clear()
            self._powered_off.set()