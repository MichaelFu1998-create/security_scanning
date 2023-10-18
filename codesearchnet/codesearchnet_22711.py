def NormalizePath(path):
    '''
    Normalizes a path maintaining the final slashes.

    Some environment variables need the final slash in order to work.

    Ex. The SOURCES_DIR set by subversion must end with a slash because of the way it is used
    in the Visual Studio projects.

    :param unicode path:
        The path to normalize.

    :rtype: unicode
    :returns:
        Normalized path
    '''
    if path.endswith('/') or path.endswith('\\'):
        slash = os.path.sep
    else:
        slash = ''
    return os.path.normpath(path) + slash