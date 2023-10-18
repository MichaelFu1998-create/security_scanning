def _moveCachedFile(from_key, to_key):
    ''' Move a file atomically within the cache: used to make cached files
        available at known keys, so they can be used by other processes.
    '''
    cache_dir = folders.cacheDirectory()
    from_path = os.path.join(cache_dir, from_key)
    to_path   = os.path.join(cache_dir, to_key)
    try:
        os.rename(from_path, to_path)
        # if moving the actual file was successful, then try to move the
        # metadata:
        os.rename(from_path+'.json', to_path+'.json')
    except Exception as e:
        # if the source doesn't exist, or the destination doesn't exist, remove
        # the file instead.
        # windows error 183 == file already exists
        # (be careful not to use WindowsError on non-windows platforms as it
        # isn't defined)
        if (isinstance(e, OSError) and e.errno == errno.ENOENT) or \
           (isinstance(e, getattr(__builtins__, "WindowsError", type(None))) and e.errno == 183):
            fsutils.rmF(from_path)
        else:
            raise