def _getModelPickleFilePath(saveModelDir):
    """ Return the absolute path of the model's pickle file.

    :param saveModelDir: (string)
           Directory of where the experiment is to be or was saved
    :returns: (string) An absolute path.
    """
    path = os.path.join(saveModelDir, "model.pkl")
    path = os.path.abspath(path)
    return path