def _create_pattern_set(self, pattern, values):
        """Create a new pattern set."""
        type_ = self._get_type(values)
        version = self._get_version(values)
        comment = values.get(COMMENT)
        self._pattern_set = self._spec.new_pattern_set(
            type_, version, pattern, self, comment
        )