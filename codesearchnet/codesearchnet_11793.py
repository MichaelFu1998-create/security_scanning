def _set_defaults(self):
        """
        Wrapper around the overrideable set_defaults().
        """

        # Register an "enabled" flag on all satchels.
        # How this flag is interpreted depends on the individual satchel.
        _prefix = '%s_enabled' % self.name
        if _prefix not in env:
            env[_prefix] = True

        # Do a one-time init of custom defaults.
        _key = '_%s' % self.name
        if _key not in env:
            env[_key] = True
            self.set_defaults()