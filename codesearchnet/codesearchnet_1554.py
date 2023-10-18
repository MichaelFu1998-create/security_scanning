def _getModelExtraDataDir(saveModelDir):
    """ Return the absolute path to the directory where the model's own
    "extra data" are stored (i.e., data that's too big for pickling).

    :param saveModelDir: (string)
           Directory of where the experiment is to be or was saved
    :returns: (string) An absolute path.
    """
    path = os.path.join(saveModelDir, "modelextradata")
    path = os.path.abspath(path)

    return path