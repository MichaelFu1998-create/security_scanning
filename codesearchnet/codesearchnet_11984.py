def read_lcc_csvlc(lcfile):
    '''This reads a CSV LC produced by an `LCC-Server
    <https://github.com/waqasbhatti/lcc-server>`_ instance.

    Parameters
    ----------

    lcfile : str
        The LC file to read.

    Returns
    -------

    dict
        Returns an lcdict that's readable by most astrobase functions for
        further processing.

    '''

    # read in the file and split by lines
    if '.gz' in os.path.basename(lcfile):
        infd = gzip.open(lcfile,'rb')
    else:
        infd = open(lcfile,'rb')

    lctext = infd.read().decode()
    infd.close()

    lctextlines = lctext.split('\n')

    lcformat = lctextlines[0]
    commentchar = lctextlines[1]

    lcstart = lctextlines.index('%s LIGHTCURVE' % commentchar)
    headerlines = lctextlines[:lcstart+1]
    lclines = lctextlines[lcstart+1:]

    metadata, columns, separator = _parse_csv_header_lcc_csv_v1(headerlines)

    # break out the objectid and objectinfo
    objectid = metadata['objectid']['val']
    objectinfo = {key:metadata[key]['val'] for key in metadata}

    # figure out the column dtypes
    colnames = []
    colnum = []
    coldtypes = []

    # generate the args for np.genfromtxt
    for k in columns:

        coldef = columns[k]
        colnames.append(k)
        colnum.append(coldef['colnum'])
        coldtypes.append(coldef['dtype'])

    coldtypes = ','.join(coldtypes)

    # read in the LC
    recarr = np.genfromtxt(
        lclines,
        comments=commentchar,
        delimiter=separator,
        usecols=colnum,
        autostrip=True,
        names=colnames,
        dtype=coldtypes
    )

    lcdict = {x:recarr[x] for x in colnames}
    lcdict['lcformat'] = lcformat
    lcdict['objectid'] = objectid
    lcdict['objectinfo'] = objectinfo
    lcdict['columns'] = colnames

    lcdict['coldefs'] = columns
    lcdict['metadata'] = metadata

    return lcdict