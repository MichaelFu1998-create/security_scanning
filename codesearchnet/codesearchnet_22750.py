def DumpDirHashToStringIO(directory, stringio, base='', exclude=None, include=None):
    '''
    Helper to iterate over the files in a directory putting those in the passed StringIO in ini
    format.

    :param unicode directory:
        The directory for which the hash should be done.

    :param StringIO stringio:
        The string to which the dump should be put.

    :param unicode base:
        If provided should be added (along with a '/') before the name=hash of file.

    :param unicode exclude:
        Pattern to match files to exclude from the hashing. E.g.: *.gz

    :param unicode include:
        Pattern to match files to include in the hashing. E.g.: *.zip
    '''
    import fnmatch
    import os

    files = [(os.path.join(directory, i), i) for i in os.listdir(directory)]
    files = [i for i in files if os.path.isfile(i[0])]
    for fullname, filename in files:
        if include is not None:
            if not fnmatch.fnmatch(fullname, include):
                continue

        if exclude is not None:
            if fnmatch.fnmatch(fullname, exclude):
                continue

        md5 = Md5Hex(fullname)
        if base:
            stringio.write('%s/%s=%s\n' % (base, filename, md5))
        else:
            stringio.write('%s=%s\n' % (filename, md5))