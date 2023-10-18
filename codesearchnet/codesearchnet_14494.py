def _save_config(self, filename=None):
        """
        Save the given user configuration.
        """
        if filename is None:
            filename = self._config_filename
        parent_path = os.path.dirname(filename)
        if not os.path.isdir(parent_path):
            os.makedirs(parent_path)
        with open(filename, "w") as configfile:
            self._config.write(configfile)