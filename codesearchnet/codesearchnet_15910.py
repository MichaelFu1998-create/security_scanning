def is_rarfile(filename):
    """Return true if file is a valid RAR file."""
    mode = constants.RAR_OM_LIST_INCSPLIT
    archive = unrarlib.RAROpenArchiveDataEx(filename, mode=mode)
    try:
        handle = unrarlib.RAROpenArchiveEx(ctypes.byref(archive))
    except unrarlib.UnrarException:
        return False
    unrarlib.RARCloseArchive(handle)
    return (archive.OpenResult == constants.SUCCESS)