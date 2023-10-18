def execute(self):
        """
        Execute one cpu instruction in the current thread (only one supported).
        :rtype: bool
        :return: C{True}

        :todo: This is where we could implement a simple schedule.
        """
        try:
            self.current.execute()
            self.clocks += 1
            if self.clocks % 10000 == 0:
                self.check_timers()
                self.sched()
        except Interruption as e:
            if e.N != 0x80:
                raise
            try:
                self.int80(self.current)
            except RestartSyscall:
                pass

        return True