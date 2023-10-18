def _sm_to_pain(self, *args, **kwargs):
        """
        Start the blockade event
        """
        _logger.info("Starting chaos for blockade %s" % self._blockade_name)
        self._do_blockade_event()
        # start the timer to end the pain
        millisec = random.randint(self._run_min_time, self._run_max_time)
        self._timer = threading.Timer(millisec / 1000.0, self.event_timeout)
        self._timer.start()