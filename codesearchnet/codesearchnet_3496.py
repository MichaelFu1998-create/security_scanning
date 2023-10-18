def wait(self, readfds, writefds, timeout):
        """ Wait for file descriptors or timeout.
            Adds the current process in the correspondent waiting list and
            yield the cpu to another running process.
        """
        logger.debug("WAIT:")
        logger.debug(f"\tProcess {self._current} is going to wait for [ {readfds!r} {writefds!r} {timeout!r} ]")
        logger.debug(f"\tProcess: {self.procs!r}")
        logger.debug(f"\tRunning: {self.running!r}")
        logger.debug(f"\tRWait: {self.rwait!r}")
        logger.debug(f"\tTWait: {self.twait!r}")
        logger.debug(f"\tTimers: {self.timers!r}")

        for fd in readfds:
            self.rwait[fd].add(self._current)
        for fd in writefds:
            self.twait[fd].add(self._current)
        if timeout is not None:
            self.timers[self._current] = self.clocks + timeout
        procid = self._current
        # self.sched()
        next_index = (self.running.index(procid) + 1) % len(self.running)
        self._current = self.running[next_index]
        logger.debug(f"\tTransfer control from process {procid} to {self._current}")
        logger.debug(f"\tREMOVING {procid!r} from {self.running!r}. Current: {self._current!r}")
        self.running.remove(procid)
        if self._current not in self.running:
            logger.debug("\tCurrent not running. Checking for timers...")
            self._current = None
            self.check_timers()