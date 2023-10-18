def _win32_is_hardlinked(fpath1, fpath2):
    """
    Test if two hard links point to the same location

    CommandLine:
        python -m ubelt._win32_links _win32_is_hardlinked

    Example:
        >>> # xdoc: +REQUIRES(WIN32)
        >>> import ubelt as ub
        >>> root = ub.ensure_app_cache_dir('ubelt', 'win32_hardlink')
        >>> ub.delete(root)
        >>> ub.ensuredir(root)
        >>> fpath1 = join(root, 'fpath1')
        >>> fpath2 = join(root, 'fpath2')
        >>> ub.touch(fpath1)
        >>> ub.touch(fpath2)
        >>> fjunc1 = _win32_junction(fpath1, join(root, 'fjunc1'))
        >>> fjunc2 = _win32_junction(fpath2, join(root, 'fjunc2'))
        >>> assert _win32_is_hardlinked(fjunc1, fpath1)
        >>> assert _win32_is_hardlinked(fjunc2, fpath2)
        >>> assert not _win32_is_hardlinked(fjunc2, fpath1)
        >>> assert not _win32_is_hardlinked(fjunc1, fpath2)
    """
    # NOTE: jwf.samefile(fpath1, fpath2) seems to behave differently
    def get_read_handle(fpath):
        if os.path.isdir(fpath):
            dwFlagsAndAttributes = jwfs.api.FILE_FLAG_BACKUP_SEMANTICS
        else:
            dwFlagsAndAttributes = 0
        hFile = jwfs.api.CreateFile(fpath, jwfs.api.GENERIC_READ,
                                    jwfs.api.FILE_SHARE_READ, None,
                                    jwfs.api.OPEN_EXISTING,
                                    dwFlagsAndAttributes, None)
        return hFile

    def get_unique_id(hFile):
        info = jwfs.api.BY_HANDLE_FILE_INFORMATION()
        res = jwfs.api.GetFileInformationByHandle(hFile, info)
        jwfs.handle_nonzero_success(res)
        unique_id = (info.volume_serial_number, info.file_index_high,
                     info.file_index_low)
        return unique_id

    hFile1 = get_read_handle(fpath1)
    hFile2 = get_read_handle(fpath2)
    try:
        are_equal = (get_unique_id(hFile1) == get_unique_id(hFile2))
    except Exception:
        raise
    finally:
        jwfs.api.CloseHandle(hFile1)
        jwfs.api.CloseHandle(hFile2)
    return are_equal