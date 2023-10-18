def _sm_relieve_pain(self, *args, **kwargs):
        """
        End the blockade event and return to a steady state
        """
        _logger.info(
                "Ending the degradation for blockade %s" % self._blockade_name)
        self._do_reset_all()
        # set a timer for the next pain event
        millisec = random.randint(self._start_min_delay, self._start_max_delay)
        self._timer = threading.Timer(millisec/1000.0, self.event_timeout)
        self._timer.start()