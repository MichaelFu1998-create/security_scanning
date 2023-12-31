def _write_checkplot_picklefile(checkplotdict,
                                outfile=None,
                                protocol=None,
                                outgzip=False):

    '''This writes the checkplotdict to a (gzipped) pickle file.

    Parameters
    ----------

    checkplotdict : dict
        This the checkplotdict to write to the pickle file.

    outfile : None or str
        The path to the output pickle file to write. If `outfile` is None,
        writes a (gzipped) pickle file of the form:

        checkplot-{objectid}.pkl(.gz)

        to the current directory.

    protocol : int
        This sets the pickle file protocol to use when writing the pickle:

        If None, will choose a protocol using the following rules:

        - 4 -> default in Python >= 3.4 - fast but incompatible with Python 2
        - 3 -> default in Python 3.0-3.3 - mildly fast
        - 2 -> default in Python 2 - very slow, but compatible with Python 2/3

        The default protocol kwarg is None, this will make an automatic choice
        for pickle protocol that's best suited for the version of Python in
        use. Note that this will make pickles generated by Py3 incompatible with
        Py2.

    outgzip : bool
        If this is True, will gzip the output file. Note that if the `outfile`
        str ends in a gzip, this will be automatically turned on.

    Returns
    -------

    str
        The absolute path to the written checkplot pickle file. None if writing
        fails.

    '''

    # figure out which protocol to use
    # for Python >= 3.4; use v4 by default
    if ((sys.version_info[0:2] >= (3,4) and not protocol) or
        (protocol > 2)):
        protocol = 4

    elif ((sys.version_info[0:2] >= (3,0) and not protocol) or
          (protocol > 2)):
        protocol = 3

    # for Python == 2.7; use v2
    elif sys.version_info[0:2] == (2,7) and not protocol:
        protocol = 2

    # otherwise, if left unspecified, use the slowest but most compatible
    # protocol. this will be readable by all (most?) Pythons
    elif not protocol:
        protocol = 0


    if outgzip:

        if not outfile:

            outfile = (
                'checkplot-{objectid}.pkl.gz'.format(
                    objectid=squeeze(checkplotdict['objectid']).replace(' ','-')
                )
            )

        with gzip.open(outfile,'wb') as outfd:
            pickle.dump(checkplotdict,outfd,protocol=protocol)

    else:

        if not outfile:

            outfile = (
                'checkplot-{objectid}.pkl'.format(
                    objectid=squeeze(checkplotdict['objectid']).replace(' ','-')
                )
            )

        # make sure to do the right thing if '.gz' is in the filename but
        # outgzip was False
        if outfile.endswith('.gz'):

            LOGWARNING('output filename ends with .gz but kwarg outgzip=False. '
                       'will use gzip to compress the output pickle')
            with gzip.open(outfile,'wb') as outfd:
                pickle.dump(checkplotdict,outfd,protocol=protocol)

        else:
            with open(outfile,'wb') as outfd:
                pickle.dump(checkplotdict,outfd,protocol=protocol)

    return os.path.abspath(outfile)