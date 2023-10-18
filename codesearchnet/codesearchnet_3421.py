def update(self, name: str, value=None, default=None, description: str=None):
        """
        Like add, but can tolerate existing values; also updates the value.

        Mostly used for setting fields from imported INI files and modified CLI flags.
        """
        if name in self._vars:
            description = description or self._vars[name].description
            default = default or self._vars[name].default
        elif name == 'name':
            raise ConfigError("'name' is a reserved name for a group.")

        v = _Var(name, description=description, default=default, defined=False)
        v.value = value
        self._vars[name] = v