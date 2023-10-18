def _read_checkplot_picklefile(checkplotpickle):
    '''This reads a checkplot gzipped pickle file back into a dict.

    NOTE: the try-except is for Python 2 pickles that have numpy arrays in
    them. Apparently, these aren't compatible with Python 3. See here:

    http://stackoverflow.com/q/11305790

    The workaround is noted in this answer:

    http://stackoverflow.com/a/41366785

    Parameters
    ----------

    checkplotpickle : str
        The path to a checkplot pickle file. This can be a gzipped file (in
        which case the file extension should end in '.gz')

    Returns
    -------

    dict
        This returns a checkplotdict.

    '''

    if checkplotpickle.endswith('.gz'):

        try:
            with gzip.open(checkplotpickle,'rb') as infd:
                cpdict = pickle.load(infd)

        except UnicodeDecodeError:

            with gzip.open(checkplotpickle,'rb') as infd:
                cpdict = pickle.load(infd, encoding='latin1')

    else:

        try:
            with open(checkplotpickle,'rb') as infd:
                cpdict = pickle.load(infd)

        except UnicodeDecodeError:

            with open(checkplotpickle,'rb') as infd:
                cpdict = pickle.load(infd, encoding='latin1')

    return cpdict