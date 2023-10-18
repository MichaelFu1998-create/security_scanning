def number_pdbs(*args, **kwargs):
    """Rename pdbs x1.pdb ... x345.pdb --> x0001.pdb ... x0345.pdb

    :Arguments:
       - *args*: filenames or glob patterns (such as "pdb/md*.pdb")
       - *format*: format string including keyword *num* ["%(num)04d"]
    """

    format = kwargs.pop('format', "%(num)04d")
    name_format = "%(prefix)s" + format +".%(suffix)s"

    for f in itertools.chain.from_iterable(map(glob.glob, args)):
        m = NUMBERED_PDB.search(f)
        if m is None:
            continue
        num = int(m.group('NUMBER'))
        prefix = m.group('PREFIX')
        suffix = m.group('SUFFIX')
        newname = name_format % vars()
        logger.info("Renaming {f!r} --> {newname!r}".format(**vars()))
        try:
            os.rename(f, newname)
        except OSError:
            logger.exception("renaming failed")