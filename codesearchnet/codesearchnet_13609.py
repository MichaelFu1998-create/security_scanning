def _set_state(self, state):
        """Set `_state` and notify any threads waiting for the change.
        """
        logger.debug(" _set_state({0!r})".format(state))
        self._state = state
        self._state_cond.notify()