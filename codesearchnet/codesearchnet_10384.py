def cat(f=None, o=None):
    """Concatenate files *f*=[...] and write to *o*"""
    # need f, o to be compatible with trjcat and eneconv
    if f is None or o is None:
        return
    target = o
    infiles = asiterable(f)
    logger.debug("cat {0!s} > {1!s} ".format(" ".join(infiles), target))
    with open(target, 'w') as out:
        rc = subprocess.call(['cat'] + infiles, stdout=out)
    if rc != 0:
        msg = "failed with return code {0:d}: cat {1!r} > {2!r} ".format(rc, " ".join(infiles), target)
        logger.exception(msg)
        raise OSError(errno.EIO, msg, target)