def pruneCache():
    ''' Prune the cache '''
    cache_dir = folders.cacheDirectory()
    def fullpath(f):
        return os.path.join(cache_dir, f)
    def getMTimeSafe(f):
        # it's possible that another process removed the file before we stat
        # it, handle this gracefully
        try:
            return os.stat(f).st_mtime
        except FileNotFoundError:
            import time
            return time.clock()
    # ensure cache exists
    fsutils.mkDirP(cache_dir)
    max_cached_modules = getMaxCachedModules()
    for f in sorted(
            [f for f in os.listdir(cache_dir) if
                os.path.isfile(fullpath(f)) and not f.endswith('.json') and not f.endswith('.locked')
            ],
            key = lambda f: getMTimeSafe(fullpath(f)),
            reverse = True
        )[max_cached_modules:]:
        cache_logger.debug('cleaning up cache file %s', f)
        removeFromCache(f)
    cache_logger.debug('cache pruned to %s items', max_cached_modules)