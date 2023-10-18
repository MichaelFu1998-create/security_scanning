def read_model_table(modelfile):
    '''
    This reads a downloaded TRILEGAL model file.

    Parameters
    ----------

    modelfile : str
        Path to the downloaded model file to read.

    Returns
    -------

    np.recarray
        Returns the model table as a Numpy record array.

    '''

    infd = gzip.open(modelfile)
    model = np.genfromtxt(infd,names=True)
    infd.close()

    return model