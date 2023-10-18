def DeleteFile(target_filename):
    '''
    Deletes the given local filename.

    .. note:: If file doesn't exist this method has no effect.

    :param unicode target_filename:
        A local filename

    :raises NotImplementedForRemotePathError:
        If trying to delete a non-local path

    :raises FileOnlyActionError:
        Raised when filename refers to a directory.
    '''
    _AssertIsLocal(target_filename)

    try:
        if IsLink(target_filename):
            DeleteLink(target_filename)
        elif IsFile(target_filename):
            os.remove(target_filename)
        elif IsDir(target_filename):
            from ._exceptions import FileOnlyActionError
            raise FileOnlyActionError(target_filename)
    except Exception as e:
        reraise(e, 'While executing filesystem.DeleteFile(%s)' % (target_filename))