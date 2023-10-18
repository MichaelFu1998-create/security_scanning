def add_extension_if_needed(filepath, ext, check_if_exists=False):
    """Add the extension ext to fpath if it doesn't have it.

    Parameters
    ----------
    filepath: str
    File name or path

    ext: str
    File extension

    check_if_exists: bool

    Returns
    -------
    File name or path with extension added, if needed.
    """
    if not filepath.endswith(ext):
        filepath += ext

    if check_if_exists:
        if not op.exists(filepath):
            raise IOError('File not found: ' + filepath)

    return filepath