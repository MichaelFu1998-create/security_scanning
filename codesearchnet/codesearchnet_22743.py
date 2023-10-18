def _AssertIsLocal(path):
    '''
    Checks if a given path is local, raise an exception if not.

    This is used in filesystem functions that do not support remote operations yet.

    :param unicode path:

    :raises NotImplementedForRemotePathError:
        If the given path is not local
    '''
    from six.moves.urllib.parse import urlparse
    if not _UrlIsLocal(urlparse(path)):
        from ._exceptions import NotImplementedForRemotePathError
        raise NotImplementedForRemotePathError