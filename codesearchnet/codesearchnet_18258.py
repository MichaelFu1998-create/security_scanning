def _get_underlying_data(self, instance):
        """Return data from raw data store, rather than overridden
        __get__ methods. Should NOT be overwritten.
        """
        self._touch(instance)
        return self.data.get(instance, None)