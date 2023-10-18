def copy_w_plus(src, dst):
    """Copy file from `src` path to `dst` path. If `dst` already exists, will add '+' characters
    to the end of the basename without extension.

    Parameters
    ----------
    src: str

    dst: str

    Returns
    -------
    dstpath: str
    """
    dst_ext = get_extension(dst)
    dst_pre = remove_ext   (dst)

    while op.exists(dst_pre + dst_ext):
        dst_pre += '+'

    shutil.copy(src, dst_pre + dst_ext)

    return dst_pre + dst_ext