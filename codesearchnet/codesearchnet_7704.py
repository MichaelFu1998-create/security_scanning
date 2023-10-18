def config_start(self):
        """
        Start a configuration session.
        For managing router admin functionality (ie allowing/blocking devices)
        """
        _LOGGER.info("Config start")

        success, _ = self._make_request(
            SERVICE_DEVICE_CONFIG, "ConfigurationStarted", {"NewSessionID": SESSION_ID})

        self.config_started = success
        return success