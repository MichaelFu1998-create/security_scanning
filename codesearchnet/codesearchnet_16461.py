def is_ignored(cls, path, patterns):
        """Check whether a path is ignored. For directories, include a trailing slash."""
        status = None
        for pattern in cls.find_matching(path, patterns):
            status = pattern.is_exclude
        return status