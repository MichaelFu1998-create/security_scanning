def get_extension(filepath, check_if_exists=False, allowed_exts=ALLOWED_EXTS):
    """Return the extension of fpath.

    Parameters
    ----------
    fpath: string
    File name or path

    check_if_exists: bool

    allowed_exts: dict
    Dictionary of strings, where the key if the last part of a complex ('.' separated) extension
    and the value is the previous part.
    For example: for the '.nii.gz' extension I would have a dict as {'.gz': ['.nii',]}

    Returns
    -------
    str
    The extension of the file name or path
    """
    if check_if_exists:
        if not op.exists(filepath):
            raise IOError('File not found: ' + filepath)

    rest, ext = op.splitext(filepath)
    if ext in allowed_exts:
        alloweds = allowed_exts[ext]
        _, ext2 = op.splitext(rest)
        if ext2 in alloweds:
            ext = ext2 + ext

    return ext