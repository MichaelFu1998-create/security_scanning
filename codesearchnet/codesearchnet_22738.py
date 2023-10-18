def GetMTime(path):
    '''
    :param unicode path:
        Path to file or directory

    :rtype: float
    :returns:
        Modification time for path.

        If this is a directory, the highest mtime from files inside it will be returned.

    @note:
        In some Linux distros (such as CentOs, or anything with ext3), mtime will not return a value
        with resolutions higher than a second.

        http://stackoverflow.com/questions/2428556/os-path-getmtime-doesnt-return-fraction-of-a-second
    '''
    _AssertIsLocal(path)

    if os.path.isdir(path):
        files = FindFiles(path)

        if len(files) > 0:
            return max(map(os.path.getmtime, files))

    return os.path.getmtime(path)