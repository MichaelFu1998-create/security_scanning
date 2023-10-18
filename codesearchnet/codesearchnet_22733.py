def ListFiles(directory):
    '''
    Lists the files in the given directory

    :type directory: unicode | unicode
    :param directory:
        A directory or URL

    :rtype: list(unicode) | list(unicode)
    :returns:
        List of filenames/directories found in the given directory.
        Returns None if the given directory does not exists.

        If `directory` is a unicode string, all files returned will also be unicode

    :raises NotImplementedProtocol:
        If file protocol is not local or FTP

    .. seealso:: FTP LIMITATIONS at this module's doc for performance issues information
    '''
    from six.moves.urllib.parse import urlparse
    directory_url = urlparse(directory)

    # Handle local
    if _UrlIsLocal(directory_url):
        if not os.path.isdir(directory):
            return None
        return os.listdir(directory)

    # Handle FTP
    elif directory_url.scheme == 'ftp':
        from ._exceptions import NotImplementedProtocol
        raise NotImplementedProtocol(directory_url.scheme)
    else:
        from ._exceptions import NotImplementedProtocol
        raise NotImplementedProtocol(directory_url.scheme)