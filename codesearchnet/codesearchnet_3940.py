def _win32_junction(path, link, verbose=0):
    """
    On older (pre 10) versions of windows we need admin privledges to make
    symlinks, however junctions seem to work.

    For paths we do a junction (softlink) and for files we use a hard link

    CommandLine:
        python -m ubelt._win32_links _win32_junction

    Example:
        >>> # xdoc: +REQUIRES(WIN32)
        >>> import ubelt as ub
        >>> root = ub.ensure_app_cache_dir('ubelt', 'win32_junction')
        >>> ub.delete(root)
        >>> ub.ensuredir(root)
        >>> fpath = join(root, 'fpath.txt')
        >>> dpath = join(root, 'dpath')
        >>> fjunc = join(root, 'fjunc.txt')
        >>> djunc = join(root, 'djunc')
        >>> ub.touch(fpath)
        >>> ub.ensuredir(dpath)
        >>> ub.ensuredir(join(root, 'djunc_fake'))
        >>> ub.ensuredir(join(root, 'djunc_fake with space'))
        >>> ub.touch(join(root, 'djunc_fake with space file'))
        >>> _win32_junction(fpath, fjunc)
        >>> _win32_junction(dpath, djunc)
        >>> # thank god colons are not allowed
        >>> djunc2 = join(root, 'djunc2 [with pathological attrs]')
        >>> _win32_junction(dpath, djunc2)
        >>> _win32_is_junction(djunc)
        >>> ub.writeto(join(djunc, 'afile.txt'), 'foo')
        >>> assert ub.readfrom(join(dpath, 'afile.txt')) == 'foo'
        >>> ub.writeto(fjunc, 'foo')
    """
    # junctions store absolute paths
    path = os.path.abspath(path)
    link = os.path.abspath(link)

    from ubelt import util_cmd
    if os.path.isdir(path):
        # try using a junction (soft link)
        if verbose:
            print('... as soft link')

        # TODO: what is the windows api for this?
        command = 'mklink /J "{}" "{}"'.format(link, path)
    else:
        # try using a hard link
        if verbose:
            print('... as hard link')
        # command = 'mklink /H "{}" "{}"'.format(link, path)
        try:
            jwfs.link(path, link)  # this seems to be allowed
        except Exception:
            print('Failed to hardlink link={} to path={}'.format(link, path))
            raise
        command = None

    if command is not None:
        info = util_cmd.cmd(command, shell=True)
        if info['ret'] != 0:
            from ubelt import util_format
            print('Failed command:')
            print(info['command'])
            print(util_format.repr2(info, nl=1))
            raise OSError(str(info))
    return link