def runtime_values(self, **kwargs):
        """
        =====API DOCS=====
        Context manager that temporarily override runtime level configurations.

        :param kwargs: Keyword arguments specifying runtime configuration settings.
        :type kwargs: arbitrary keyword arguments
        :returns: N/A

        :Example:

        >>> import tower_cli
        >>> from tower_cli.conf import settings
        >>> with settings.runtime_values(username='user', password='pass'):
        >>>     print(tower_cli.get_resource('credential').list())

        =====API DOCS=====
        """

        # Coerce all values to strings (to be coerced back by configparser
        # later) and defenestrate any None values.
        for k, v in copy.copy(kwargs).items():
            # If the value is None, just get rid of it.
            if v is None:
                kwargs.pop(k)
                continue

            # Remove these keys from the cache, if they are present.
            self._cache.pop(k, None)

            # Coerce values to strings.
            kwargs[k] = six.text_type(v)

        # Replace the `self._runtime` INI parser with a new one, using
        # the context manager's kwargs as the "defaults" (there can never
        # be anything other than defaults, but that isn't a problem for our
        # purposes because we're using our own precedence system).
        #
        # Ensure that everything is put back to rights at the end of the
        # context manager call.
        old_runtime_parser = self._runtime
        try:
            self._runtime = Parser(defaults=kwargs)
            self._runtime.add_section('general')
            yield self
        finally:
            # Revert the runtime configparser object.
            self._runtime = old_runtime_parser

            # Remove the keys from the cache again, since the settings
            # have been reverted.
            for key in kwargs:
                self._cache.pop(k, None)