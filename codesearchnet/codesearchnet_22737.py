def DeleteDirectory(directory, skip_on_error=False):
    '''
    Deletes a directory.

    :param unicode directory:

    :param bool skip_on_error:
        If True, ignore any errors when trying to delete directory (for example, directory not
        found)

    :raises NotImplementedForRemotePathError:
        If trying to delete a remote directory.
    '''
    _AssertIsLocal(directory)

    import shutil
    def OnError(fn, path, excinfo):
        '''
        Remove the read-only flag and try to remove again.
        On Windows, rmtree fails when trying to remove a read-only file. This fix it!
        Another case: Read-only directories return True in os.access test. It seems that read-only
        directories has it own flag (looking at the property windows on Explorer).
        '''
        if IsLink(path):
            return

        if fn is os.remove and os.access(path, os.W_OK):
            raise

        # Make the file WRITEABLE and executes the original delete function (osfunc)
        import stat
        os.chmod(path, stat.S_IWRITE)
        fn(path)

    try:
        if not os.path.isdir(directory):
            if skip_on_error:
                return
            from ._exceptions import DirectoryNotFoundError
            raise DirectoryNotFoundError(directory)
        shutil.rmtree(directory, onerror=OnError)
    except:
        if not skip_on_error:
            raise