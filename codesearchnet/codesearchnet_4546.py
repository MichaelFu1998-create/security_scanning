def make_callback(self, kind=None):
        """Makes the callback and resets the timer.
        """
        self._wake_up_time = time.time() + self.interval
        self.callback(*self.cb_args)