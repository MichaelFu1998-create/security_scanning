def end_timing(self):
        """
        Completes measuring time interval and updates counter.
        """

        if self._callback != None:
            elapsed = time.clock() * 1000 - self._start
            self._callback.end_timing(self._counter, elapsed)