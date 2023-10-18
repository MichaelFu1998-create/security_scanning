def OpenFile(filename, binary=False, newline=None, encoding=None):
    '''
    Open a file and returns it.
    Consider the possibility of a remote file (HTTP, HTTPS, FTP)

    :param unicode filename:
        Local or remote filename.

    :param bool binary:
        If True returns the file as is, ignore any EOL conversion.
        If set ignores univeral_newlines parameter.

    :param None|''|'\n'|'\r'|'\r\n' newline:
        Controls universal newlines.
        See 'io.open' newline parameter documentation for more details.

    :param unicode encoding:
        File's encoding. If not None, contents obtained from file will be decoded using this
        `encoding`.

    :returns file:
        The open file, it must be closed by the caller

    @raise: FileNotFoundError
        When the given filename cannot be found

    .. seealso:: FTP LIMITATIONS at this module's doc for performance issues information
    '''
    from six.moves.urllib.parse import urlparse
    filename_url = urlparse(filename)

    # Check if file is local
    if _UrlIsLocal(filename_url):
        if not os.path.isfile(filename):
            from ._exceptions import FileNotFoundError
            raise FileNotFoundError(filename)

        mode = 'rb' if binary else 'r'
        return io.open(filename, mode, encoding=encoding, newline=newline)

    # Not local
    from ._exceptions import NotImplementedProtocol
    raise NotImplementedProtocol(target_url.scheme)