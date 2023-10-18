def _sm_start(self, *args, **kwargs):
        """
        Start the timer waiting for pain
        """
        millisec = random.randint(self._start_min_delay, self._start_max_delay)
        self._timer = threading.Timer(millisec / 1000.0, self.event_timeout)
        self._timer.start()