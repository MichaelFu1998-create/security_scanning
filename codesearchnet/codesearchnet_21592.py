def get_configuration(self, key, default=None):
        """Returns the configuration for KEY"""
        if key in self.config:
            return self.config.get(key)
        else:
            return default