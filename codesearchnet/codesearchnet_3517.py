def sched(self):
        """ Yield CPU.
            This will choose another process from the RUNNNIG list and change
            current running process. May give the same cpu if only one running
            process.
        """
        if len(self.procs) > 1:
            logger.info("SCHED:")
            logger.info("\tProcess: %r", self.procs)
            logger.info("\tRunning: %r", self.running)
            logger.info("\tRWait: %r", self.rwait)
            logger.info("\tTWait: %r", self.twait)
            logger.info("\tTimers: %r", self.timers)
            logger.info("\tCurrent clock: %d", self.clocks)
            logger.info("\tCurrent cpu: %d", self._current)

        if len(self.running) == 0:
            logger.info("None running checking if there is some process waiting for a timeout")
            if all([x is None for x in self.timers]):
                raise Deadlock()
            self.clocks = min([x for x in self.timers if x is not None]) + 1
            self.check_timers()
            assert len(self.running) != 0, "DEADLOCK!"
            self._current = self.running[0]
            return
        next_index = (self.running.index(self._current) + 1) % len(self.running)
        next = self.running[next_index]
        if len(self.procs) > 1:
            logger.info("\tTransfer control from process %d to %d", self._current, next)
        self._current = next