def savetxt2(fname, X, delimiter=' ', newline='\n', comment_character='#',
        header='', save_dtype=False, fmt={}):

    """ format of table header:

        # ID [type]:name(index) .... * number of items

        user's header is not prefixed by comment_character

        name of nested dtype elements are split by .
    """
    prefixfmt = {}
    for key in fmt:
            prefixfmt[key] = fmt[key]

    olddtype = X.dtype
    newdtype = flatten_dtype(numpy.dtype([('', (X.dtype, X.shape[1:]))]))
    X = X.view(dtype=newdtype)
    dtype = X.dtype
    X = numpy.atleast_1d(X.squeeze())
    header2 = _mkheader(dtype)
    fmtstr = _mkfmtstr(dtype, prefixfmt, delimiter, _default_fmt)
    if hasattr(fname, 'write'):
        fh = fname
        cleanup = lambda : None
    else:
        fh = file(fname, 'w+')
        cleanup = lambda : fh.close()
    try:
        fh.write (header)
        if header[:-1] != newline:
            fh.write(newline)
        fh.write (comment_character)
        fh.write ('!')
        fh.write (header2)
        fh.write (delimiter)
        fh.write ('*%d' % len(X))
        fh.write(newline)
        if save_dtype:
            fh.write (comment_character)
            fh.write ('?')
            fh.write (base64.b64encode(pickle.dumps(olddtype)))
            fh.write (newline)
        for row in X:
            fh.write(fmtstr % tuple(row))
            fh.write(newline)

        if hasattr(fh, 'flush'):
            fh.flush()
    finally:
        cleanup()