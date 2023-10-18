def is_redirecting(path):
    '''Returns True if path contains a .cpenv file'''

    candidate = unipath(path, '.cpenv')
    return os.path.exists(candidate) and os.path.isfile(candidate)