def augpath(path, suffix='', prefix='', ext=None, base=None, multidot=False):
    """
    Augments a path with a new basename, extension, prefix and/or suffix.

    A prefix is inserted before the basename. A suffix is inserted
    between the basename and the extension. The basename and extension can be
    replaced with a new one.

    Args:
        path (PathLike): string representation of a path
        suffix (str): placed between the basename and extension
        prefix (str): placed in front of the basename
        ext (str): if specified, replaces the extension
        base (str): if specified, replaces the basename (without extension)
        multidot (bool): if False, everything after the last dot in the
            basename is the extension. If True, everything after the first dot
            in the basename is the extension (Defaults to False).

    Returns:
        PathLike: augmented path

    CommandLine:
        python -m ubelt.util_path augpath

    Example:
        >>> import ubelt as ub
        >>> path = 'foo.bar'
        >>> suffix = '_suff'
        >>> prefix = 'pref_'
        >>> ext = '.baz'
        >>> newpath = ub.augpath(path, suffix, prefix, ext=ext, base='bar')
        >>> print('newpath = %s' % (newpath,))
        newpath = pref_bar_suff.baz

    Example:
        >>> augpath('foo.bar')
        'foo.bar'
        >>> augpath('foo.bar', ext='.BAZ')
        'foo.BAZ'
        >>> augpath('foo.bar', suffix='_')
        'foo_.bar'
        >>> augpath('foo.bar', prefix='_')
        '_foo.bar'
        >>> augpath('foo.bar', base='baz')
        'baz.bar'
        >>> augpath('foo.tar.gz', ext='.zip', multidot=True)
        foo.zip
        >>> augpath('foo.tar.gz', ext='.zip', multidot=False)
        foo.tar.zip
    """
    # Breakup path
    dpath, fname = split(path)
    if multidot:
        parts = fname.split('.')
        fname_noext = '.'.join(parts[:1])
        orig_ext = '.'.join(parts[1:])
    else:
        fname_noext, orig_ext = splitext(fname)
    ext = orig_ext if ext is None else ext
    fname_noext = fname_noext if base is None else base
    # Augment and recombine into new path
    new_fname = ''.join((prefix, fname_noext, suffix, ext))
    newpath = join(dpath, new_fname)
    return newpath