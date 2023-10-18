def unpackFromCache(cache_key, to_directory):
    ''' If the specified cache key exists, unpack the tarball into the
        specified directory, otherwise raise NotInCache (a KeyError subclass).
    '''
    if cache_key is None:
        raise NotInCache('"None" is never in cache')

    cache_key = _encodeCacheKey(cache_key)

    cache_dir = folders.cacheDirectory()
    fsutils.mkDirP(cache_dir)
    path = os.path.join(cache_dir, cache_key)
    logger.debug('attempt to unpack from cache %s -> %s', path, to_directory)
    try:
        unpackFrom(path, to_directory)
        try:
            shutil.copy(path + '.json', os.path.join(to_directory, '.yotta_origin.json'))
        except IOError as e:
            if e.errno == errno.ENOENT:
                pass
            else:
                raise
        cache_logger.debug('unpacked %s from cache into %s', cache_key, to_directory)
        return
    except IOError as e:
        if e.errno == errno.ENOENT:
            cache_logger.debug('%s not in cache', cache_key)
            raise NotInCache('not in cache')
    except OSError as e:
        if e.errno == errno.ENOTEMPTY:
            logger.error('directory %s was not empty: probably simultaneous invocation of yotta! It is likely that downloaded sources are corrupted.')
        else:
            raise