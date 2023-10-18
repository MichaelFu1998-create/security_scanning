def MoveDirectory(source_dir, target_dir):
    '''
    Moves a directory.

    :param unicode source_dir:

    :param unicode target_dir:

    :raises NotImplementedError:
        If trying to move anything other than:
            Local dir -> local dir
            FTP dir -> FTP dir (same host)
    '''
    if not IsDir(source_dir):
        from ._exceptions import DirectoryNotFoundError
        raise DirectoryNotFoundError(source_dir)

    if Exists(target_dir):
        from ._exceptions import DirectoryAlreadyExistsError
        raise DirectoryAlreadyExistsError(target_dir)

    from six.moves.urllib.parse import urlparse
    source_url = urlparse(source_dir)
    target_url = urlparse(target_dir)

    # Local to local
    if _UrlIsLocal(source_url) and _UrlIsLocal(target_url):
        import shutil
        shutil.move(source_dir, target_dir)

    # FTP to FTP
    elif source_url.scheme == 'ftp' and target_url.scheme == 'ftp':
        from ._exceptions import NotImplementedProtocol
        raise NotImplementedProtocol(target_url.scheme)
    else:
        raise NotImplementedError('Can only move directories local->local or ftp->ftp')