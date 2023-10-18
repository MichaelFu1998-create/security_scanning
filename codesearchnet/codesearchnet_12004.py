def read_csv_lightcurve(lcfile):
    '''
    This reads in a K2 lightcurve in CSV format. Transparently reads gzipped
    files.

    Parameters
    ----------

    lcfile : str
        The light curve file to read.

    Returns
    -------

    dict
        Returns an lcdict.

    '''

    # read in the file first
    if '.gz' in os.path.basename(lcfile):
        LOGINFO('reading gzipped K2 LC: %s' % lcfile)
        infd = gzip.open(lcfile,'rb')
    else:
        LOGINFO('reading K2 LC: %s' % lcfile)
        infd = open(lcfile,'rb')

    lctext = infd.read().decode()
    infd.close()

    # figure out the header and get the LC columns
    lcstart = lctext.index('# LIGHTCURVE\n')
    lcheader = lctext[:lcstart+12]
    lccolumns = lctext[lcstart+13:].split('\n')
    lccolumns = [x.split(',') for x in lccolumns if len(x) > 0]

    # initialize the lcdict and parse the CSV header
    lcdict = _parse_csv_header(lcheader)

    # tranpose the LC rows into columns
    lccolumns = list(zip(*lccolumns))

    # write the columns to the dict
    for colind, col in enumerate(lcdict['columns']):

        # this picks out the caster to use when reading each column using the
        # definitions in the lcutils.COLUMNDEFS dictionary
        lcdict[col.lower()] = np.array([COLUMNDEFS[col][2](x)
                                        for x in lccolumns[colind]])

    lcdict['columns'] = [x.lower() for x in lcdict['columns']]

    return lcdict