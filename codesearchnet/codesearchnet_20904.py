def _effective_filename(self):
        # type: () -> str
        """
        Returns the filename which is effectively used by the application. If
        overridden by an environment variable, it will return that filename.
        """
        # same logic for the configuration filename. First, check if we were
        # initialized with a filename...
        config_filename = ''
        if self.filename:
            config_filename = self.filename

        # ... next, take the value from the environment
        env_filename = getenv(self.env_filename_name)
        if env_filename:
            self._log.info('Configuration filename was overridden with %r '
                           'by the environment variable %s.',
                           env_filename,
                           self.env_filename_name)
            config_filename = env_filename

        return config_filename