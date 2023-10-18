def loadfile(filepath, mmap_mode=None):
    """
    :param filepath:
    :param mmap_mode: {None, ‘r+’, ‘r’, ‘w+’, ‘c’} see. joblib.load
    :return:
    """
    import joblib

    try:
        return joblib.load(filepath, mmap_mode=mmap_mode)
    except IOError:
        return None