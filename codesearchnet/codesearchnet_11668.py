def unpackTarballStream(stream, into_directory, hash={}, cache_key=None, origin_info=dict()):
    ''' Unpack a responses stream that contains a tarball into a directory. If
        a hash is provided, then it will be used as a cache key (for future
        requests you can try to retrieve the key value from the cache first,
        before making the request)
    '''
    cache_key = _encodeCacheKey(cache_key)

    # if the cache is disabled, then use a random cache key even if one was
    # provided, so that the module is not persisted in the cache and its
    # temporary download location is a random key:
    if getMaxCachedModules() == 0:
        cache_key = None

    new_cache_key = _downloadToCache(stream, hash, origin_info)
    unpackFromCache(new_cache_key, into_directory)

    if cache_key is None:
        # if we didn't provide a cache key, there's no point in storing the cache
        removeFromCache(new_cache_key)
    else:
        # otherwise make this file available at the known cache key
        _moveCachedFile(new_cache_key, cache_key)