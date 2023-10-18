def read_csvlc(lcfile):
    '''This reads a HAT data server or LCC-Server produced CSV light curve
    into an lcdict.

    This will automatically figure out the format of the file
    provided. Currently, it can read:

    - legacy HAT data server CSV LCs (e.g. from
      https://hatsouth.org/planets/lightcurves.html) with an extension of the
      form: `.hatlc.csv.gz`.
    - all LCC-Server produced LCC-CSV-V1 LCs (e.g. from
      https://data.hatsurveys.org) with an extension of the form: `-csvlc.gz`.


    Parameters
    ----------

    lcfile : str
        The light curve file to read.

    Returns
    -------

    dict
        Returns an lcdict that can be read and used by many astrobase processing
        functions.

    '''

    # read in the file and split by lines
    if '.gz' in os.path.basename(lcfile):
        LOGINFO('reading gzipped HATLC: %s' % lcfile)
        infd = gzip.open(lcfile,'rb')
    else:
        LOGINFO('reading HATLC: %s' % lcfile)
        infd = open(lcfile,'rb')


    # this transparently reads LCC CSVLCs
    lcformat_check = infd.read(12).decode()
    if 'LCC-CSVLC' in lcformat_check:
        infd.close()
        return read_lcc_csvlc(lcfile)
    else:
        infd.seek(0)

    # below is reading the HATLC v2 CSV LCs

    lctext = infd.read().decode()  # argh Python 3
    infd.close()

    # figure out the header and get the LC columns
    lcstart = lctext.index('# LIGHTCURVE\n')
    lcheader = lctext[:lcstart+12]
    lccolumns = lctext[lcstart+13:].split('\n')
    lccolumns = [x for x in lccolumns if len(x) > 0]

    # initialize the lcdict and parse the CSV header
    lcdict = _parse_csv_header(lcheader)

    # tranpose the LC rows into columns
    lccolumns = [x.split(',') for x in lccolumns]
    lccolumns = list(zip(*lccolumns))  # argh more Python 3

    # write the columns to the dict
    for colind, col in enumerate(lcdict['columns']):

        if (col.split('_')[0] in LC_MAG_COLUMNS or
            col.split('_')[0] in LC_ERR_COLUMNS or
            col.split('_')[0] in LC_FLAG_COLUMNS):
            lcdict[col] = np.array([_smartcast(x,
                                               COLUMNDEFS[col.split('_')[0]][2])
                                    for x in lccolumns[colind]])

        elif col in COLUMNDEFS:
            lcdict[col] = np.array([_smartcast(x,COLUMNDEFS[col][2])
                                    for x in lccolumns[colind]])

        else:
            LOGWARNING('lcdict col %s has no formatter available' % col)
            continue

    return lcdict