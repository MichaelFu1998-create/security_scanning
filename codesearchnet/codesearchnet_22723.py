def IsDir(directory):
    '''
    :param unicode directory:
        A path

    :rtype: bool
    :returns:
        Returns whether the given path points to an existent directory.

    :raises NotImplementedProtocol:
        If the path protocol is not local or ftp

    .. seealso:: FTP LIMITATIONS at this module's doc for performance issues information
    '''
    from six.moves.urllib.parse import urlparse
    directory_url = urlparse(directory)

    if _UrlIsLocal(directory_url):
        return os.path.isdir(directory)
    elif directory_url.scheme == 'ftp':
        from ._exceptions import NotImplementedProtocol
        raise NotImplementedProtocol(target_url.scheme)
    else:
        from ._exceptions import NotImplementedProtocol
        raise NotImplementedProtocol(directory_url.scheme)