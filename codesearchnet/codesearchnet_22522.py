def prepare_path(path):
    """
    Path join helper method
    Join paths if list passed

    :type path: str|unicode|list
    :rtype: str|unicode
    """
    if type(path) == list:
        return os.path.join(*path)
    return path