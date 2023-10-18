def bounds(self):
        """Process bounds as defined in the configuration."""
        if self._raw["bounds"] is None:
            return self.process_pyramid.bounds
        else:
            return Bounds(*_validate_bounds(self._raw["bounds"]))