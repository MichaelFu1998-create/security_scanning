def _win32_can_symlink(verbose=0, force=0, testing=0):
    """
    CommandLine:
        python -m ubelt._win32_links _win32_can_symlink

    Example:
        >>> # xdoc: +REQUIRES(WIN32)
        >>> import ubelt as ub
        >>> _win32_can_symlink(verbose=1, force=1, testing=1)
    """
    global __win32_can_symlink__
    if verbose:
        print('__win32_can_symlink__ = {!r}'.format(__win32_can_symlink__))
    if __win32_can_symlink__ is not None and not force:
        return __win32_can_symlink__

    from ubelt import util_platform
    tempdir = util_platform.ensure_app_cache_dir('ubelt', '_win32_can_symlink')

    util_io.delete(tempdir)
    util_path.ensuredir(tempdir)

    dpath = join(tempdir, 'dpath')
    fpath = join(tempdir, 'fpath.txt')

    dlink = join(tempdir, 'dlink')
    flink = join(tempdir, 'flink.txt')

    util_path.ensuredir(dpath)
    util_io.touch(fpath)

    # Add broken variants of the links for testing purposes
    # Its ugly, but so is all this windows code.
    if testing:
        broken_dpath = join(tempdir, 'broken_dpath')
        broken_fpath = join(tempdir, 'broken_fpath.txt')
        # Create files that we will delete after we link to them
        util_path.ensuredir(broken_dpath)
        util_io.touch(broken_fpath)

    try:
        _win32_symlink(dpath, dlink)
        if testing:
            _win32_symlink(broken_dpath, join(tempdir, 'broken_dlink'))
        can_symlink_directories = os.path.islink(dlink)
    except OSError:
        can_symlink_directories = False
    if verbose:
        print('can_symlink_directories = {!r}'.format(can_symlink_directories))

    try:
        _win32_symlink(fpath, flink)
        if testing:
            _win32_symlink(broken_fpath, join(tempdir, 'broken_flink'))
        can_symlink_files = os.path.islink(flink)
        # os.path.islink(flink)
    except OSError:
        can_symlink_files = False
    if verbose:
        print('can_symlink_files = {!r}'.format(can_symlink_files))

    assert int(can_symlink_directories) + int(can_symlink_files) != 1, (
        'can do one but not both. Unexpected {} {}'.format(
            can_symlink_directories, can_symlink_files))

    try:
        # test that we can create junctions, even if symlinks are disabled
        djunc = _win32_junction(dpath, join(tempdir, 'djunc'))
        fjunc = _win32_junction(fpath, join(tempdir, 'fjunc.txt'))
        if testing:
            _win32_junction(broken_dpath, join(tempdir, 'broken_djunc'))
            _win32_junction(broken_fpath, join(tempdir, 'broken_fjunc.txt'))
        assert _win32_is_junction(djunc)
        assert _win32_is_hardlinked(fpath, fjunc)
    except Exception:
        warnings.warn('We cannot create junctions either!')
        raise

    if testing:
        # break the links
        util_io.delete(broken_dpath)
        util_io.delete(broken_fpath)

        if verbose:
            from ubelt import util_links
            util_links._dirstats(tempdir)

    try:
        # Cleanup the test directory
        util_io.delete(tempdir)
    except Exception:
        print('ERROR IN DELETE')
        from ubelt import util_links
        util_links._dirstats(tempdir)
        raise

    can_symlink = can_symlink_directories and can_symlink_files
    __win32_can_symlink__ = can_symlink
    if not can_symlink:
        warnings.warn('Cannot make real symlink. Falling back to junction')

    if verbose:
        print('can_symlink = {!r}'.format(can_symlink))
        print('__win32_can_symlink__ = {!r}'.format(__win32_can_symlink__))
    return can_symlink