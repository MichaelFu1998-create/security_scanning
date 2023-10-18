def MoveFile(source_filename, target_filename):
    '''
    Moves a file.

    :param unicode source_filename:

    :param unicode target_filename:

    :raises NotImplementedForRemotePathError:
        If trying to operate with non-local files.
    '''
    _AssertIsLocal(source_filename)
    _AssertIsLocal(target_filename)

    import shutil
    shutil.move(source_filename, target_filename)