def write_config(self):
        """Writes `self.cfg` to `self.config_file`."""
        with open(self.config_file, "w") as config_file:
            self.cfg.write(config_file)