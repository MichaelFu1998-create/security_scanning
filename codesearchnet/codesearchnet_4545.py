def make_callback(self, kind=None):
        """Makes the callback and resets the timer.

        KWargs:
               - kind (str): Default=None, used to pass information on what
                 triggered the callback
        """
        self._wake_up_time = time.time() + self.interval
        self.callback(tasks=self._event_buffer, kind=kind)
        self._event_buffer = []