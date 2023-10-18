def _sm_stop_from_pain(self, *args, **kwargs):
        """
        Stop chaos while there is a blockade event in progress
        """
        _logger.info("Stopping chaos for blockade %s" % self._blockade_name)
        self._do_reset_all()