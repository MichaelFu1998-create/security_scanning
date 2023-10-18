def _open(name_or_fdesc, mode='r', fmt='auto'):
    '''An intelligent wrapper for ``open``.

    Parameters
    ----------
    name_or_fdesc : string-type or open file descriptor
        If a string type, refers to the path to a file on disk.

        If an open file descriptor, it is returned as-is.

    mode : string
        The mode with which to open the file.
        See ``open`` for details.

    fmt : string ['auto', 'jams', 'json', 'jamz']
        The encoding for the input/output stream.

        If `auto`, the format is inferred from the filename extension.

        Otherwise, use the specified coding.


    See Also
    --------
    open
    gzip.open
    '''

    open_map = {'jams': open,
                'json': open,
                'jamz': gzip.open,
                'gz': gzip.open}

    # If we've been given an open descriptor, do the right thing
    if hasattr(name_or_fdesc, 'read') or hasattr(name_or_fdesc, 'write'):
        yield name_or_fdesc

    elif isinstance(name_or_fdesc, six.string_types):
        # Infer the opener from the extension

        if fmt == 'auto':
            _, ext = os.path.splitext(name_or_fdesc)

            # Pull off the extension separator
            ext = ext[1:]
        else:
            ext = fmt

        try:
            ext = ext.lower()

            # Force text mode if we're using gzip
            if ext in ['jamz', 'gz'] and 't' not in mode:
                mode = '{:s}t'.format(mode)

            with open_map[ext](name_or_fdesc, mode=mode) as fdesc:
                yield fdesc

        except KeyError:
            raise ParameterError('Unknown JAMS extension '
                                 'format: "{:s}"'.format(ext))

    else:
        # Don't know how to handle this. Raise a parameter error
        raise ParameterError('Invalid filename or '
                             'descriptor: {}'.format(name_or_fdesc))