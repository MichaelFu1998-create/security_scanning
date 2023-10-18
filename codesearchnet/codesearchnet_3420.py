def add(self, name: str, default=None, description: str=None):
        """
        Add a variable named |name| to this value group, optionally giving it a
        default value and a description.

        Variables must be added with this method before they can be set or read.
        Reading a variable replaces the variable that was defined previously, but
        updates the description if a new one is set.

        """
        if name in self._vars:
            raise ConfigError(f"{self.name}.{name} already defined.")

        if name == 'name':
            raise ConfigError("'name' is a reserved name for a group.")

        v = _Var(name, description=description, default=default)
        self._vars[name] = v