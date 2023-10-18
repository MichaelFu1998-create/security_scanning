def get(self, name, default, allow_default=True):
        """ Return a setting value.

            :param str name: Setting key name.
            :param default: Default value of setting if it's not explicitly
                            set.
            :param bool allow_default: If true, use the parameter default as
                            default if the key is not set, else raise
                            :exc:`LookupError`
            :raises: :exc:`LookupError` if allow_default is false and the setting is
                     not set.
        """
        if not self.settings.get('pyconfig.case_sensitive', False):
            name = name.lower()
        if name not in self.settings:
            if not allow_default:
                raise LookupError('No setting "{name}"'.format(name=name))
            self.settings[name] = default
        return self.settings[name]