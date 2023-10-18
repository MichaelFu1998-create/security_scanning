def kepler_lcdict_to_pkl(lcdict, outfile=None):
    '''This writes the `lcdict` to a Python pickle.

    Parameters
    ----------

    lcdict : lcdict
        This is the input `lcdict` to write to a pickle.

    outfile : str or None
        If this is None, the object's Kepler ID/EPIC ID will determined from the
        `lcdict` and used to form the filename of the output pickle file. If
        this is a `str`, the provided filename will be used.

    Returns
    -------

    str
        The absolute path to the written pickle file.

    '''

    if not outfile:
        outfile = '%s-keplc.pkl' % lcdict['objectid'].replace(' ','-')

    # we're using pickle.HIGHEST_PROTOCOL here, this will make Py3 pickles
    # unreadable for Python 2.7
    with open(outfile,'wb') as outfd:
        pickle.dump(lcdict, outfd, protocol=pickle.HIGHEST_PROTOCOL)

    return os.path.abspath(outfile)