def _win32_symlink2(path, link, allow_fallback=True, verbose=0):
    """
    Perform a real symbolic link if possible. However, on most versions of
    windows you need special privledges to create a real symlink. Therefore, we
    try to create a symlink, but if that fails we fallback to using a junction.

    AFAIK, the main difference between symlinks and junctions are that symlinks
    can reference relative or absolute paths, where as junctions always
    reference absolute paths. Not 100% on this though. Windows is weird.

    Note that junctions will not register as links via `islink`, but I
    believe real symlinks will.
    """
    if _win32_can_symlink():
        return _win32_symlink(path, link, verbose)
    else:
        return _win32_junction(path, link, verbose)