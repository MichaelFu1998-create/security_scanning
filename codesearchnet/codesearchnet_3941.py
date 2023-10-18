def _win32_is_junction(path):
    """
    Determines if a path is a win32 junction

    CommandLine:
        python -m ubelt._win32_links _win32_is_junction

    Example:
        >>> # xdoc: +REQUIRES(WIN32)
        >>> import ubelt as ub
        >>> root = ub.ensure_app_cache_dir('ubelt', 'win32_junction')
        >>> ub.delete(root)
        >>> ub.ensuredir(root)
        >>> dpath = join(root, 'dpath')
        >>> djunc = join(root, 'djunc')
        >>> ub.ensuredir(dpath)
        >>> _win32_junction(dpath, djunc)
        >>> assert _win32_is_junction(djunc) is True
        >>> assert _win32_is_junction(dpath) is False
        >>> assert _win32_is_junction('notafile') is False
    """
    if not exists(path):
        if os.path.isdir(path):
            if not os.path.islink(path):
                return True
        return False
    return jwfs.is_reparse_point(path) and not os.path.islink(path)