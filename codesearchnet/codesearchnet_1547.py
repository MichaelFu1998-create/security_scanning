def _getModelCheckpointFilePath(checkpointDir):
    """ Return the absolute path of the model's checkpoint file.

    :param checkpointDir: (string)
           Directory of where the experiment is to be or was saved
    :returns: (string) An absolute path.
    """
    path = os.path.join(checkpointDir, "model.data")
    path = os.path.abspath(path)
    return path