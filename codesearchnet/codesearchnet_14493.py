def _read_config(self, filename=None):
        """
        Read the user configuration
        """
        if filename:
            self._config_filename = filename
        else:
            try:
                import appdirs
            except ImportError:
                raise Exception("Missing dependency for determining config path. Please install "
                                "the 'appdirs' Python module.")
            self._config_filename = appdirs.user_config_dir(_LIBRARY_NAME, "ProfitBricks") + ".ini"
        if not self._config:
            self._config = configparser.ConfigParser()
            self._config.optionxform = str
            self._config.read(self._config_filename)