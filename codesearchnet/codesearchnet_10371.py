def anyopen(datasource, mode='rt', reset=True):
    """Open datasource (gzipped, bzipped, uncompressed) and return a stream.

    `datasource` can be a filename or a stream (see :func:`isstream`). By
    default, a stream is reset to its start if possible (via
    :meth:`~io.IOBase.seek` or :meth:`~cString.StringIO.reset`).

    If possible, the attribute ``stream.name`` is set to the filename or
    "<stream>" if no filename could be associated with the *datasource*.

    :Arguments:
      *datasource*
        a file (from :class:`file` or :func:`open`) or a stream (e.g. from
        :func:`urllib2.urlopen` or :class:`cStringIO.StringIO`)
      *mode*
        {'r', 'w', 'a'} (optional),
        Open in r(ead), w(rite) or a(ppen) mode. More complicated
        modes ('r+', 'w+', ...) are not supported; only the first letter of
        `mode` is used and thus any additional modifiers are silently ignored.
      *reset*
        bool (optional),
        try to read (`mode` 'r') the stream from the start

    :Returns:
       file-like object


    .. SeeAlso::
       :func:`openany` to be used with the :keyword:`with` statement.

    """
    handlers = {'bz2': bz2_open, 'gz': gzip.open, '': open}

    if mode.startswith('r'):
        if isstream(datasource):
            stream = datasource
            try:
                filename = str(stream.name)  # maybe that does not always work?
            except AttributeError:
                filename = "<stream>"
            if reset:
                try:
                    stream.reset()
                except (AttributeError, IOError):
                    try:
                        stream.seek(0)
                    except (AttributeError, IOError):
                        warnings.warn("Stream {0}: not guaranteed to be at the beginning."
                                      "".format(filename),
                                      category=StreamWarning)
        else:
            stream = None
            filename = datasource
            for ext in ('bz2', 'gz', ''):  # file == '' should be last
                openfunc = handlers[ext]
                stream = _get_stream(datasource, openfunc, mode=mode)
                if stream is not None:
                    break
            if stream is None:
                raise IOError(errno.EIO, "Cannot open file or stream in mode={mode!r}.".format(**vars()), repr(filename))
    elif mode.startswith('w') or mode.startswith('a'):  # append 'a' not tested...
        if isstream(datasource):
            stream = datasource
            try:
                filename = str(stream.name)  # maybe that does not always work?
            except AttributeError:
                filename = "<stream>"
        else:
            stream = None
            filename = datasource
            name, ext = os.path.splitext(filename)
            if ext.startswith('.'):
                ext = ext[1:]
            if not ext in ('bz2', 'gz'):
                ext = ''  # anything else but bz2 or gz is just a normal file
            openfunc = handlers[ext]
            stream = openfunc(datasource, mode=mode)
            if stream is None:
                raise IOError(errno.EIO, "Cannot open file or stream in mode={mode!r}.".format(**vars()), repr(filename))
    else:
        raise NotImplementedError("Sorry, mode={mode!r} is not implemented for {datasource!r}".format(**vars()))
    try:
        stream.name = filename
    except (AttributeError, TypeError):
        pass  # can't set name (e.g. cStringIO.StringIO)
    return stream