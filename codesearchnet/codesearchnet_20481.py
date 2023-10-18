def copy_w_ext(srcfile, destdir, basename):
    """ Copy `srcfile` in `destdir` with name `basename + get_extension(srcfile)`.
    Add pluses to the destination path basename if a file with the same name already
    exists in `destdir`.

    Parameters
    ----------
    srcfile: str

    destdir: str

    basename:str

    Returns
    -------
    dstpath: str
    """

    ext = get_extension(op.basename(srcfile))

    dstpath = op.join(destdir, basename + ext)

    return copy_w_plus(srcfile, dstpath)