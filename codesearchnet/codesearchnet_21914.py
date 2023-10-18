def expandpath(path):
    '''Returns an absolute expanded path'''

    return os.path.abspath(os.path.expandvars(os.path.expanduser(path)))