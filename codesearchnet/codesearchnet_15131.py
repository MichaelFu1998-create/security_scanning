def _fill_pattern_collection(self, pattern_collection, values):
        """Fill a pattern collection."""
        pattern = values.get(PATTERNS, [])
        for pattern_to_parse in pattern:
            parsed_pattern = self._pattern(pattern_to_parse)
            pattern_collection.append(parsed_pattern)