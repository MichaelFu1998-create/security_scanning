def from_file(cls, file):
        """Try loading given config file.

        :param str file: full path to the config file to load
        """
        if not os.path.exists(file):
            raise ValueError("Config file not found.")

        try:
            config_parser = configparser.ConfigParser()
            config_parser.read(file)

            configuration = cls(file, config_parser)
            if not configuration.check_config_sanity():
                raise ValueError("Error in config file.")
            else:
                return configuration
        except configparser.Error:
            raise ValueError("Config file is invalid.")