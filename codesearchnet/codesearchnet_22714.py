def NormStandardPath(path):
    '''
    Normalizes a standard path (posixpath.normpath) maintaining any slashes at the end of the path.

    Normalize:
        Removes any local references in the path "/../"

    StandardPath:
        We are defining that the standard-path is the one with only back-slashes in it, either
        on Windows or any other platform.
    '''
    import posixpath
    if path.endswith('/'):
        slash = '/'
    else:
        slash = ''
    return posixpath.normpath(path) + slash