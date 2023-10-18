def read_hatlc(hatlc):
    '''
    This reads a consolidated HAT LC written by the functions above.

    Returns a dict.

    '''

    lcfname = os.path.basename(hatlc)

    # unzip the files first
    if '.gz' in lcfname:
        lcf = gzip.open(hatlc,'rb')
    elif '.bz2' in lcfname:
        lcf = bz2.BZ2File(hatlc, 'rb')
    else:
        lcf = open(hatlc,'rb')

    if '.fits' in lcfname and HAVEPYFITS:

        hdulist = pyfits.open(lcf)
        objectinfo = hdulist[0].header
        objectlc = hdulist[1].data
        lccols = objectlc.columns.names
        hdulist.close()
        lcf.close()

        lcdict = {}

        for col in lccols:
            lcdict[col] = np.array(objectlc[col])

        lcdict['hatid'] = objectinfo['hatid']
        lcdict['twomassid'] = objectinfo['2massid']
        lcdict['ra'] = objectinfo['ra']
        lcdict['dec'] = objectinfo['dec']
        lcdict['mags'] = [objectinfo[x] for x in ('vmag','rmag','imag',
                                                  'jmag','hmag','kmag')]
        lcdict['ndet'] = objectinfo['ndet']
        lcdict['hatstations'] = objectinfo['hats']
        lcdict['filters'] = objectinfo['filters']
        lcdict['columns'] = lccols

        return lcdict

    elif '.fits' in lcfname and not HAVEPYFITS:

        print("can't read %s since we don't have the pyfits module" % lcfname)
        return

    elif '.csv' in lcfname or '.hatlc' in lcfname:

        lcflines = lcf.read().decode().split('\n')
        lcf.close()

        # now process the read-in LC
        objectdata = [x for x in lcflines if x.startswith('#')]
        objectlc = [x for x in lcflines if not x.startswith('#')]
        objectlc = [x for x in objectlc if len(x) > 1]

        if '.csv' in lcfname:
            objectlc = [x.split(',') for x in objectlc]
        else:
            objectlc = [x.split() for x in objectlc]

        # transpose split rows to get columns
        objectlc = list(zip(*objectlc))

        # read the header to figure out the object's info and column names
        objectdata = [x.strip('#') for x in objectdata]
        objectdata = [x.strip() for x in objectdata]
        objectdata = [x for x in objectdata if len(x) > 0]

        hatid, twomassid = objectdata[0].split(' - ')
        ra, dec = objectdata[1].split(', ')
        ra = float(ra.split(' = ')[-1].strip(' deg'))
        dec = float(dec.split(' = ')[-1].strip(' deg'))

        vmag, rmag, imag, jmag, hmag, kmag = objectdata[2].split(', ')
        vmag = float(vmag.split(' = ')[-1])
        rmag = float(rmag.split(' = ')[-1])
        imag = float(imag.split(' = ')[-1])
        jmag = float(jmag.split(' = ')[-1])
        hmag = float(hmag.split(' = ')[-1])
        kmag = float(kmag.split(' = ')[-1])

        ndet = int(objectdata[3].split(': ')[-1])
        hatstations = objectdata[4].split(': ')[-1]

        filterhead_ind = objectdata.index('Filters used:')
        columnhead_ind = objectdata.index('Columns:')

        filters = objectdata[filterhead_ind:columnhead_ind]

        columndefs = objectdata[columnhead_ind+1:]

        columns = []
        for line in columndefs:

            colnum, colname, coldesc = line.split(' - ')
            columns.append(colname)

        lcdict = {}

        # now write all the columns to the output dictionary
        for ind, col in enumerate(columns):

            # this formats everything nicely using our existing column
            # definitions
            lcdict[col] = np.array([TEXTLC_OUTPUT_COLUMNS[col][3](x)
                                    for x in objectlc[ind]])

        # write the object metadata to the output dictionary
        lcdict['hatid'] = hatid
        lcdict['twomassid'] = twomassid.replace('2MASS J','')
        lcdict['ra'] = ra
        lcdict['dec'] = dec
        lcdict['mags'] = [vmag, rmag, imag, jmag, hmag, kmag]
        lcdict['ndet'] = ndet
        lcdict['hatstations'] = hatstations.split(', ')
        lcdict['filters'] = filters[1:]
        lcdict['cols'] = columns

        return lcdict