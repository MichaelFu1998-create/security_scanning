def wait(self, readfds, writefds, timeout):
        """ Wait for filedescriptors or timeout.
            Adds the current process to the corresponding waiting list and
            yields the cpu to another running process.
        """
        logger.info("WAIT:")
        logger.info("\tProcess %d is going to wait for [ %r %r %r ]", self._current, readfds, writefds, timeout)
        logger.info("\tProcess: %r", self.procs)
        logger.info("\tRunning: %r", self.running)
        logger.info("\tRWait: %r", self.rwait)
        logger.info("\tTWait: %r", self.twait)
        logger.info("\tTimers: %r", self.timers)

        for fd in readfds:
            self.rwait[fd].add(self._current)
        for fd in writefds:
            self.twait[fd].add(self._current)
        if timeout is not None:
            self.timers[self._current] = self.clocks + timeout
        else:
            self.timers[self._current] = None
        procid = self._current
        # self.sched()
        next_index = (self.running.index(procid) + 1) % len(self.running)
        self._current = self.running[next_index]
        logger.info("\tTransfer control from process %d to %d", procid, self._current)
        logger.info("\tREMOVING %r from %r. Current: %r", procid, self.running, self._current)
        self.running.remove(procid)
        if self._current not in self.running:
            logger.info("\tCurrent not running. Checking for timers...")
            self._current = None
            if all([x is None for x in self.timers]):
                raise Deadlock()
            self.check_timers()