def copy_mhd_and_raw(src, dst):
    """Copy .mhd and .raw files to dst.

    If dst is a folder, won't change the file, but if dst is another filepath,
    will modify the ElementDataFile field in the .mhd to point to the
    new renamed .raw file.

    Parameters
    ----------
    src: str
        Path to the .mhd file to be copied

    dst: str
        Path to the destination of the .mhd and .raw files.
        If a new file name is given, the extension will be ignored.

    Returns
    -------
    dst: str
    """
    # check if src exists
    if not op.exists(src):
        raise IOError('Could not find file {}.'.format(src))

    # check its extension
    ext = get_extension(src)
    if ext != '.mhd':
        msg = 'The src file path must be a .mhd file. Given: {}.'.format(src)
        raise ValueError(msg)

    # get the raw file for this src mhd file
    meta_src = _read_meta_header(src)

    # get the source raw file
    src_raw = meta_src['ElementDataFile']
    if not op.isabs(src_raw):
        src_raw = op.join(op.dirname(src), src_raw)

    # check if dst is dir
    if op.isdir(dst):
        # copy the mhd and raw file to its destiny
        shutil.copyfile(src, dst)
        shutil.copyfile(src_raw, dst)
        return dst

    # build raw file dst file name
    dst_raw = op.join(op.dirname(dst), remove_ext(op.basename(dst))) + '.raw'

    # add extension to the dst path
    if get_extension(dst) != '.mhd':
        dst += '.mhd'

    # copy the mhd and raw file to its destiny
    log.debug('cp: {} -> {}'.format(src,     dst))
    log.debug('cp: {} -> {}'.format(src_raw, dst_raw))
    shutil.copyfile(src, dst)
    shutil.copyfile(src_raw, dst_raw)

    # check if src file name is different than dst file name
    # if not the same file name, change the content of the ElementDataFile field
    if op.basename(dst) != op.basename(src):
        log.debug('modify {}: ElementDataFile: {} -> {}'.format(dst, src_raw,
                                                                op.basename(dst_raw)))
        meta_dst = _read_meta_header(dst)
        meta_dst['ElementDataFile'] = op.basename(dst_raw)
        write_meta_header(dst, meta_dst)

    return dst