def discover(cls):
        """Make a guess about the config file location an try loading it."""
        file = os.path.join(Config.config_dir, Config.config_name)
        return cls.from_file(file)