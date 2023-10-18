def from_file(cls, file, *args, **kwargs):
        """Try loading given cache file."""
        try:
            cache = shelve.open(file)
            return cls(file, cache, *args, **kwargs)
        except OSError as e:
            logger.debug("Loading {0} failed".format(file))
            raise e