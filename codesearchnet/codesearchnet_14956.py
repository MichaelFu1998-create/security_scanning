def get_default(self):
        """
        Returns the default value for this field.
        """
        if self.has_default():
            if callable(self.default):
                default = self.default()
                if isinstance(default, uuid.UUID):
                    return default.hex
                return default
            if isinstance(self.default, uuid.UUID):
                return self.default.hex
            return self.default
        return None