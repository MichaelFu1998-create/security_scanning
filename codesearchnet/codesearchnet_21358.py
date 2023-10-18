def get(self, section, key):
        """
            This function tries to retrieve the value from the configfile
            otherwise will return a default.
        """
        try:
            return self.config.get(section, key)
        except configparser.NoSectionError:
            pass
        except configparser.NoOptionError:
            pass
        return self.defaults[section][key]