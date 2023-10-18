def sched(self):
        """ Yield CPU.
            This will choose another process from the running list and change
            current running process. May give the same cpu if only one running
            process.
        """
        if len(self.procs) > 1:
            logger.debug("SCHED:")
            logger.debug(f"\tProcess: {self.procs!r}")
            logger.debug(f"\tRunning: {self.running!r}")
            logger.debug(f"\tRWait: {self.rwait!r}")
            logger.debug(f"\tTWait: {self.twait!r}")
            logger.debug(f"\tTimers: {self.timers!r}")
            logger.debug(f"\tCurrent clock: {self.clocks}")
            logger.debug(f"\tCurrent cpu: {self._current}")

        if len(self.running) == 0:
            logger.debug("None running checking if there is some process waiting for a timeout")
            if all([x is None for x in self.timers]):
                raise Deadlock()
            self.clocks = min(x for x in self.timers if x is not None) + 1
            self.check_timers()
            assert len(self.running) != 0, "DEADLOCK!"
            self._current = self.running[0]
            return
        next_index = (self.running.index(self._current) + 1) % len(self.running)
        next_running_idx = self.running[next_index]
        if len(self.procs) > 1:
            logger.debug(f"\tTransfer control from process {self._current} to {next_running_idx}")
        self._current = next_running_idx