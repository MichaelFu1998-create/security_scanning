def CopyDirectory(source_dir, target_dir, override=False):
    '''
    Recursively copy a directory tree.

    :param unicode source_dir:
        Where files will come from

    :param unicode target_dir:
        Where files will go to

    :param bool override:
        If True and target_dir already exists, it will be deleted before copying.

    :raises NotImplementedForRemotePathError:
        If trying to copy to/from remote directories
    '''
    _AssertIsLocal(source_dir)
    _AssertIsLocal(target_dir)

    if override and IsDir(target_dir):
        DeleteDirectory(target_dir, skip_on_error=False)

    import shutil
    shutil.copytree(source_dir, target_dir)