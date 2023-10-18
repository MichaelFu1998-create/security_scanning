def get(self):
        """ Dequeue a state with the max priority """

        # A shutdown has been requested
        if self.is_shutdown():
            return None

        # if not more states in the queue, let's wait for some forks
        while len(self._states) == 0:
            # if no worker is running, bail out
            if self.running == 0:
                return None
            # if a shutdown has been requested, bail out
            if self.is_shutdown():
                return None
            # if there ares actually some workers running, wait for state forks
            logger.debug("Waiting for available states")
            self._lock.wait()

        state_id = self._policy.choice(list(self._states))
        if state_id is None:
            return None
        del self._states[self._states.index(state_id)]
        return state_id