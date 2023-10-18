def _get_username(self, username=None, use_config=True, config_filename=None):
        """Determine the username

        If a username is given, this name is used. Otherwise the configuration
        file will be consulted if `use_config` is set to True. The user is asked
        for the username if the username is not available. Then the username is
        stored in the configuration file.

        :param      username: Username (used directly if given)
        :type       username: ``str``

        :param      use_config: Whether to read username from configuration file
        :type       use_config: ``bool``

        :param      config_filename: Path to the configuration file
        :type       config_filename: ``str``

        """
        if not username and use_config:
            if self._config is None:
                self._read_config(config_filename)
            username = self._config.get("credentials", "username", fallback=None)

        if not username:
            username = input("Please enter your username: ").strip()
            while not username:
                username = input("No username specified. Please enter your username: ").strip()
            if 'credendials' not in self._config:
                self._config.add_section('credentials')
            self._config.set("credentials", "username", username)
            self._save_config()

        return username