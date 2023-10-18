def copyfileobj(fsrc, fdst, total, length=16*1024):
    """Copy data from file-like object fsrc to file-like object fdst

    This is like shutil.copyfileobj but with a progressbar.
    """
    with tqdm(unit='bytes', total=total, unit_scale=True) as pbar:
        while 1:
            buf = fsrc.read(length)
            if not buf:
                break
            fdst.write(buf)
            pbar.update(len(buf))