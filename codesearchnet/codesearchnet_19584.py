def listdir(p, match='*', exclude='', listtype='file', matchfun=None):
    """
    list file(or folder) for this path (NOT recursive)
    :param p:
    :param match:
    :param exclude:
    :param listtype: ('file' | 'filepath' |'dir' | 'all')
    :param matchfun: match fun (default fnmatch.fnmatch) True/False = matchfun(name, pattern)
    :rtype:
    """
    if listtype == 'file':
        gen = listfile(p)
    elif listtype == 'filepath':
        gen = listfilepath(p)
    elif listtype == 'dir':
        gen = listfolder(p)
    elif listtype == 'dirpath':
        gen = listfolderpath(p)
    else:  # list file or folder
        gen = (entry.name for entry in scandir.scandir(p))

    return filter_pattern(gen, match, exclude, matchfun)