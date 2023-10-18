def loadtxt2(fname, dtype=None, delimiter=' ', newline='\n', comment_character='#',
        skiplines=0):
    """ Known issues delimiter and newline is not respected. 
        string quotation with space is broken.
    """
    dtypert = [None, None, None]
    def preparedtype(dtype):
        dtypert[0] = dtype
        flatten = flatten_dtype(dtype)
        dtypert[1] = flatten
        dtypert[2] = numpy.dtype([('a', (numpy.int8,
            flatten.itemsize))])
        buf = numpy.empty((), dtype=dtypert[1])
        converters = [_default_conv[flatten[name].char] for name in flatten.names]
        return buf, converters, flatten.names

    def fileiter(fh):
        converters = []
        buf = None

        if dtype is not None:
            buf, converters, names = preparedtype(dtype)
            yield None

        for lineno, line in enumerate(fh):
            if lineno < skiplines: continue
            if line[0] in comment_character:
                if buf is None and line[1] == '?':
                    ddtype = pickle.loads(base64.b64decode(line[2:]))
                    buf, converters, names = preparedtype(ddtype)
                    yield None
                continue
            for word, c, name in zip(line.split(), converters, names):
                buf[name] = c(word)
            buf2 = buf.copy().view(dtype=dtypert[2])
            yield buf2

    if isinstance(fname, basestring):
        fh = file(fh, 'r')
        cleanup = lambda : fh.close()
    else:
        fh = iter(fname)
        cleanup = lambda : None
    try:
        i = fileiter(fh)
        i.next()
        return numpy.fromiter(i, dtype=dtypert[2]).view(dtype=dtypert[0]) 
    finally:
        cleanup()