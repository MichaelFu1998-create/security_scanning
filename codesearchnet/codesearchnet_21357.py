def set(self, section, key, value):
        """
            Creates the section value if it does not exists and sets the value.
            Use write_config to actually set the value.
        """
        if not section in self.config:
            self.config.add_section(section)
        self.config.set(section, key, value)