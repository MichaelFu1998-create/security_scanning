def symlink(real_path, link_path, overwrite=False, verbose=0):
    """
    Create a symbolic link.

    This will work on linux or windows, however windows does have some corner
    cases. For more details see notes in `ubelt._win32_links`.

    Args:
        path (PathLike): path to real file or directory
        link_path (PathLike): path to desired location for symlink
        overwrite (bool): overwrite existing symlinks.
            This will not overwrite real files on systems with proper symlinks.
            However, on older versions of windows junctions are
            indistinguishable from real files, so we cannot make this
            guarantee.  (default = False)
        verbose (int):  verbosity level (default=0)

    Returns:
        PathLike: link path

    CommandLine:
        python -m ubelt.util_links symlink:0

    Example:
        >>> import ubelt as ub
        >>> dpath = ub.ensure_app_cache_dir('ubelt', 'test_symlink0')
        >>> real_path = join(dpath, 'real_file.txt')
        >>> link_path = join(dpath, 'link_file.txt')
        >>> [ub.delete(p) for p in [real_path, link_path]]
        >>> ub.writeto(real_path, 'foo')
        >>> result = symlink(real_path, link_path)
        >>> assert ub.readfrom(result) == 'foo'
        >>> [ub.delete(p) for p in [real_path, link_path]]

    Example:
        >>> import ubelt as ub
        >>> from os.path import dirname
        >>> dpath = ub.ensure_app_cache_dir('ubelt', 'test_symlink1')
        >>> ub.delete(dpath)
        >>> ub.ensuredir(dpath)
        >>> _dirstats(dpath)
        >>> real_dpath = ub.ensuredir((dpath, 'real_dpath'))
        >>> link_dpath = ub.augpath(real_dpath, base='link_dpath')
        >>> real_path = join(dpath, 'afile.txt')
        >>> link_path = join(dpath, 'afile.txt')
        >>> [ub.delete(p) for p in [real_path, link_path]]
        >>> ub.writeto(real_path, 'foo')
        >>> result = symlink(real_dpath, link_dpath)
        >>> assert ub.readfrom(link_path) == 'foo', 'read should be same'
        >>> ub.writeto(link_path, 'bar')
        >>> _dirstats(dpath)
        >>> assert ub.readfrom(link_path) == 'bar', 'very bad bar'
        >>> assert ub.readfrom(real_path) == 'bar', 'changing link did not change real'
        >>> ub.writeto(real_path, 'baz')
        >>> _dirstats(dpath)
        >>> assert ub.readfrom(real_path) == 'baz', 'very bad baz'
        >>> assert ub.readfrom(link_path) == 'baz', 'changing real did not change link'
        >>> ub.delete(link_dpath, verbose=1)
        >>> _dirstats(dpath)
        >>> assert not exists(link_dpath), 'link should not exist'
        >>> assert exists(real_path), 'real path should exist'
        >>> _dirstats(dpath)
        >>> ub.delete(dpath, verbose=1)
        >>> _dirstats(dpath)
        >>> assert not exists(real_path)
    """
    path = normpath(real_path)
    link = normpath(link_path)

    if not os.path.isabs(path):
        # if path is not absolute it must be specified relative to link
        if _can_symlink():
            path = os.path.relpath(path, os.path.dirname(link))
        else:  # nocover
            # On windows, we need to use absolute paths
            path = os.path.abspath(path)

    if verbose:
        print('Symlink: {path} -> {link}'.format(path=path, link=link))
    if islink(link):
        if verbose:
            print('... already exists')
        pointed = _readlink(link)
        if pointed == path:
            if verbose > 1:
                print('... and points to the right place')
            return link
        if verbose > 1:
            if not exists(link):
                print('... but it is broken and points somewhere else: {}'.format(pointed))
            else:
                print('... but it points somewhere else: {}'.format(pointed))
        if overwrite:
            util_io.delete(link, verbose=verbose > 1)
    elif exists(link):
        if _win32_links is None:
            if verbose:
                print('... already exists, but its a file. This will error.')
            raise FileExistsError(
                'cannot overwrite a physical path: "{}"'.format(path))
        else:  # nocover
            if verbose:
                print('... already exists, and is either a file or hard link. '
                      'Assuming it is a hard link. '
                      'On non-win32 systems this would error.')

    if _win32_links is None:
        os.symlink(path, link)
    else:  # nocover
        _win32_links._symlink(path, link, overwrite=overwrite, verbose=verbose)

    return link