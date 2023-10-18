def CreateDirectory(directory):
    '''
    Create directory including any missing intermediate directory.

    :param unicode directory:

    :return unicode|urlparse.ParseResult:
        Returns the created directory or url (see urlparse).

    :raises NotImplementedProtocol:
        If protocol is not local or FTP.

    .. seealso:: FTP LIMITATIONS at this module's doc for performance issues information
    '''
    from six.moves.urllib.parse import urlparse
    directory_url = urlparse(directory)

    # Handle local
    if _UrlIsLocal(directory_url):
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    # Handle FTP
    elif directory_url.scheme == 'ftp':
        from ._exceptions import NotImplementedProtocol
        raise NotImplementedProtocol(directory_url.scheme)
    else:
        from ._exceptions import NotImplementedProtocol
        raise NotImplementedProtocol(directory_url.scheme)