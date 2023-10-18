def find_first(filename, suffices=None):
    """Find first *filename* with a suffix from *suffices*.

    :Arguments:
      *filename*
         base filename; this file name is checked first
      *suffices*
         list of suffices that are tried in turn on the root of *filename*; can contain the
         ext separator (:data:`os.path.extsep`) or not

    :Returns: The first match or ``None``.
    """
    # struct is not reliable as it depends on qscript so now we just try everything...

    root,extension = os.path.splitext(filename)
    if suffices is None:
        suffices = []
    else:
        suffices = withextsep(suffices)
    extensions = [extension] + suffices  # native name is first
    for ext in extensions:
        fn = root + ext
        if os.path.exists(fn):
            return fn
    return None