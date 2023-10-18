def _DoCopyFile(source_filename, target_filename, copy_symlink=True):
    '''
    :param unicode source_filename:
        The source filename.
        Schemas: local, ftp, http

    :param unicode target_filename:
        Target filename.
        Schemas: local, ftp

    :param  copy_symlink:
        @see _CopyFileLocal

    :raises FileNotFoundError:
        If source_filename does not exist
    '''
    from six.moves.urllib.parse import urlparse

    source_url = urlparse(source_filename)
    target_url = urlparse(target_filename)

    if _UrlIsLocal(source_url):
        if not Exists(source_filename):
            from ._exceptions import FileNotFoundError
            raise FileNotFoundError(source_filename)

        if _UrlIsLocal(target_url):
            # local to local
            _CopyFileLocal(source_filename, target_filename, copy_symlink=copy_symlink)
        elif target_url.scheme in ['ftp']:
            from ._exceptions import NotImplementedProtocol
            raise NotImplementedProtocol(target_url.scheme)
        else:
            from ._exceptions import NotImplementedProtocol
            raise NotImplementedProtocol(target_url.scheme)

    elif source_url.scheme in ['http', 'https', 'ftp']:
        if _UrlIsLocal(target_url):
            # HTTP/FTP to local
            from ._exceptions import NotImplementedProtocol
            raise NotImplementedProtocol(target_url.scheme)
        else:
            # HTTP/FTP to other ==> NotImplemented
            from ._exceptions import NotImplementedProtocol
            raise NotImplementedProtocol(target_url.scheme)
    else:
        from ._exceptions import NotImplementedProtocol  # @Reimport
        raise NotImplementedProtocol(source_url.scheme)