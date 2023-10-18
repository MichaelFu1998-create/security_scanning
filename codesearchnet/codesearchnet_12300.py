def read_fakelc(fakelcfile):
    '''
    This just reads a pickled fake LC.

    Parameters
    ----------

    fakelcfile : str
        The fake LC file to read.

    Returns
    -------

    dict
        This returns an lcdict.

    '''

    try:
        with open(fakelcfile,'rb') as infd:
            lcdict = pickle.load(infd)
    except UnicodeDecodeError:
        with open(fakelcfile,'rb') as infd:
            lcdict = pickle.load(infd, encoding='latin1')

    return lcdict