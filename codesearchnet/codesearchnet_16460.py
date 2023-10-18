def find_matching(cls, path, patterns):
        """Yield all matching patterns for path."""
        for pattern in patterns:
            if pattern.match(path):
                yield pattern