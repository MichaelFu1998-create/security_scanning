def get(self, key, local_default = None, required = False):
        """Get a parameter value.

        If parameter is not set, return `local_default` if it is not `None`
        or the PyXMPP global default otherwise.

        :Raise `KeyError`: if parameter has no value and no global default

        :Return: parameter value
        """
        # pylint: disable-msg=W0221
        if key in self._settings:
            return self._settings[key]
        if local_default is not None:
            return local_default
        if key in self._defs:
            setting_def = self._defs[key]
            if setting_def.default is not None:
                return setting_def.default
            factory = setting_def.factory
            if factory is None:
                return None
            value = factory(self)
            if setting_def.cache is True:
                setting_def.default = value
            return value
        if required:
            raise KeyError(key)
        return local_default