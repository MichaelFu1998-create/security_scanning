def discover(cls, *args, **kwargs):
        """Make a guess about the cache file location an try loading it."""
        file = os.path.join(Cache.cache_dir, Cache.cache_name)
        return cls.from_file(file, *args, **kwargs)