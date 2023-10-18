def add_enum(self, name, choices):
        """An enumeration-valued dimension.

        The base measure associated with this dimension is a categorical
        distribution with equal weight on each element in `choices`.
        """
        if not isinstance(choices, Iterable):
            raise ValueError('variable %s: choices must be iterable' % name)
        self.variables[name] = EnumVariable(name, choices)