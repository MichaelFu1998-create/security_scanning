def _win32_read_junction(path):
    """
    Returns the location that the junction points, raises ValueError if path is
    not a junction.

    CommandLine:
        python -m ubelt._win32_links _win32_read_junction

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
        >>> path = djunc
        >>> pointed = _win32_read_junction(path)
        >>> print('pointed = {!r}'.format(pointed))
    """
    if not jwfs.is_reparse_point(path):
        raise ValueError('not a junction')

    # --- Older version based on using shell commands ---
    # if not exists(path):
    #     if six.PY2:
    #         raise OSError('Cannot find path={}'.format(path))
    #     else:
    #         raise FileNotFoundError('Cannot find path={}'.format(path))
    # target_name = os.path.basename(path)
    # for type_or_size, name, pointed in _win32_dir(path, '*'):
    #     if type_or_size == '<JUNCTION>' and name == target_name:
    #         return pointed
    # raise ValueError('not a junction')

    # new version using the windows api
    handle = jwfs.api.CreateFile(
            path, 0, 0, None, jwfs.api.OPEN_EXISTING,
            jwfs.api.FILE_FLAG_OPEN_REPARSE_POINT |
            jwfs.api.FILE_FLAG_BACKUP_SEMANTICS,
            None)

    if handle == jwfs.api.INVALID_HANDLE_VALUE:
        raise WindowsError()

    res = jwfs.reparse.DeviceIoControl(
            handle, jwfs.api.FSCTL_GET_REPARSE_POINT, None, 10240)

    bytes = jwfs.create_string_buffer(res)
    p_rdb = jwfs.cast(bytes, jwfs.POINTER(jwfs.api.REPARSE_DATA_BUFFER))
    rdb = p_rdb.contents

    if rdb.tag not in [2684354563, jwfs.api.IO_REPARSE_TAG_SYMLINK]:
        raise RuntimeError(
                "Expected <2684354563 or 2684354572>, but got %d" % rdb.tag)

    jwfs.handle_nonzero_success(jwfs.api.CloseHandle(handle))
    subname = rdb.get_substitute_name()
    # probably has something to do with long paths, not sure
    if subname.startswith('?\\'):
        subname = subname[2:]
    return subname