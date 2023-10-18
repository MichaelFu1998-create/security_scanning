def Exists(path):
    '''
    :rtype: bool
    :returns:
        True if the path already exists (either a file or a directory)

    .. seealso:: FTP LIMITATIONS at this module's doc for performance issues information
    '''
    from six.moves.urllib.parse import urlparse
    path_url = urlparse(path)

    # Handle local
    if _UrlIsLocal(path_url):
        return IsFile(path) or IsDir(path) or IsLink(path)
    return IsFile(path) or IsDir(path)