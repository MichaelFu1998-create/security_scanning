def init_bounds(self):
        """
        Process bounds this process is currently initialized with.

        This gets triggered by using the ``init_bounds`` kwarg. If not set, it will
        be equal to self.bounds.
        """
        if self._raw["init_bounds"] is None:
            return self.bounds
        else:
            return Bounds(*_validate_bounds(self._raw["init_bounds"]))