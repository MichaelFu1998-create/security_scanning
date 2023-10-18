def kill_all(self):
        """kill all slaves and reap the monitor """
        for pid in self.children:
            try:
                os.kill(pid, signal.SIGTRAP)
            except OSError:
                continue
        self.join()