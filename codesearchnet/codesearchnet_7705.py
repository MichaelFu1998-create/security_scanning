def config_finish(self):
        """
        End of a configuration session.
        Tells the router we're done managing admin functionality.
        """
        _LOGGER.info("Config finish")
        if not self.config_started:
            return True

        success, _ = self._make_request(
            SERVICE_DEVICE_CONFIG, "ConfigurationFinished", {"NewStatus": "ChangesApplied"})

        self.config_started = not success
        return success