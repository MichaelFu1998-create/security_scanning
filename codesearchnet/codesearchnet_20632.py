def _safe_cache(memory, func, **kwargs):
    """ A wrapper for mem.cache that flushes the cache if the version
        number of nibabel has changed.
    """
    cachedir = memory.cachedir

    if cachedir is None or cachedir in __CACHE_CHECKED:
        return memory.cache(func, **kwargs)

    version_file = os.path.join(cachedir, 'module_versions.json')

    versions = dict()
    if os.path.exists(version_file):
        with open(version_file, 'r') as _version_file:
            versions = json.load(_version_file)

    modules = (nibabel, )
    # Keep only the major + minor version numbers
    my_versions = dict((m.__name__, LooseVersion(m.__version__).version[:2])
                       for m in modules)
    commons = set(versions.keys()).intersection(set(my_versions.keys()))
    collisions = [m for m in commons if versions[m] != my_versions[m]]

    # Flush cache if version collision
    if len(collisions) > 0:
        if nilearn.CHECK_CACHE_VERSION:
            warnings.warn("Incompatible cache in %s: "
                          "different version of nibabel. Deleting "
                          "the cache. Put nilearn.CHECK_CACHE_VERSION "
                          "to false to avoid this behavior."
                          % cachedir)
            try:
                tmp_dir = (os.path.split(cachedir)[:-1]
                           + ('old_%i' % os.getpid(), ))
                tmp_dir = os.path.join(*tmp_dir)
                # We use rename + unlink to be more robust to race
                # conditions
                os.rename(cachedir, tmp_dir)
                shutil.rmtree(tmp_dir)
            except OSError:
                # Another process could have removed this dir
                pass

            try:
                os.makedirs(cachedir)
            except OSError:
                # File exists?
                pass
        else:
            warnings.warn("Incompatible cache in %s: "
                          "old version of nibabel." % cachedir)

    # Write json files if configuration is different
    if versions != my_versions:
        with open(version_file, 'w') as _version_file:
            json.dump(my_versions, _version_file)

    __CACHE_CHECKED[cachedir] = True

    return memory.cache(func, **kwargs)