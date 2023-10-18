def check_timers(self):
        """ Awake process if timer has expired """
        if self._current is None:
            # Advance the clocks. Go to future!!
            advance = min([self.clocks] + [x for x in self.timers if x is not None]) + 1
            logger.debug(f"Advancing the clock from {self.clocks} to {advance}")
            self.clocks = advance
        for procid in range(len(self.timers)):
            if self.timers[procid] is not None:
                if self.clocks > self.timers[procid]:
                    self.procs[procid].PC += self.procs[procid].instruction.size
                    self.awake(procid)