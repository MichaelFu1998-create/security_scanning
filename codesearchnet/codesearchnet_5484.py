def _sm_stop_from_no_pain(self, *args, **kwargs):
        """
        Stop chaos when there is no current blockade operation
        """
        # Just stop the timer.  It is possible that it was too late and the
        # timer is about to run
        _logger.info("Stopping chaos for blockade %s" % self._blockade_name)
        self._timer.cancel()