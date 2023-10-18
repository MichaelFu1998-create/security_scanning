def IsFile(path):
    '''
    :param unicode path:
        Path to a file (local or ftp)

    :raises NotImplementedProtocol:
        If checking for a non-local, non-ftp file

    :rtype: bool
    :returns:
        True if the file exists

    .. seealso:: FTP LIMITATIONS at this module's doc for performance issues information
    '''
    from six.moves.urllib.parse import urlparse
    url = urlparse(path)

    if _UrlIsLocal(url):
        if IsLink(path):
            return IsFile(ReadLink(path))
        return os.path.isfile(path)

    elif url.scheme == 'ftp':
        from ._exceptions import NotImplementedProtocol
        raise NotImplementedProtocol(url.scheme)
    else:
        from ._exceptions import NotImplementedProtocol
        raise NotImplementedProtocol(url.scheme)