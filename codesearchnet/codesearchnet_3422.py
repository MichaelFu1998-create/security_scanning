def get_description(self, name: str) -> str:
        """
        Return the description, or a help string of variable identified by |name|.
        """
        if name not in self._vars:
            raise ConfigError(f"{self.name}.{name} not defined.")

        return self._vars[name].description