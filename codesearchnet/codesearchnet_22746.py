def CheckForUpdate(source, target):
    '''
    Checks if the given target filename should be re-generated because the source has changed.
    :param source: the source filename.
    :param target: the target filename.
    :return bool:
        True if the target is out-dated, False otherwise.
    '''
    return \
        not os.path.isfile(target) or \
        os.path.getmtime(source) > os.path.getmtime(target)