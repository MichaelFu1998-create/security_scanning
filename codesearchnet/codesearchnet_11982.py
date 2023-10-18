def _parse_csv_header(header):
    '''
    This parses the CSV header from the CSV HAT sqlitecurve.

    Returns a dict that can be used to update an existing lcdict with the
    relevant metadata info needed to form a full LC.

    '''

    # first, break into lines
    headerlines = header.split('\n')
    headerlines = [x.lstrip('# ') for x in headerlines]

    # next, find the indices of the metadata sections
    objectstart = headerlines.index('OBJECT')
    metadatastart = headerlines.index('METADATA')
    camfilterstart = headerlines.index('CAMFILTERS')
    photaperturestart = headerlines.index('PHOTAPERTURES')
    columnstart = headerlines.index('COLUMNS')
    lcstart = headerlines.index('LIGHTCURVE')

    # get the lines for the header sections
    objectinfo = headerlines[objectstart+1:metadatastart-1]
    metadatainfo = headerlines[metadatastart+1:camfilterstart-1]
    camfilterinfo = headerlines[camfilterstart+1:photaperturestart-1]
    photapertureinfo = headerlines[photaperturestart+1:columnstart-1]
    columninfo = headerlines[columnstart+1:lcstart-1]

    # parse the header sections and insert the appropriate key-val pairs into
    # the lcdict
    metadict = {'objectinfo':{}}

    # first, the objectinfo section
    objectinfo = [x.split(';') for x in objectinfo]

    for elem in objectinfo:
        for kvelem in elem:
            key, val = kvelem.split(' = ',1)
            metadict['objectinfo'][key.strip()] = (
                _smartcast(val, METAKEYS[key.strip()])
            )

    # the objectid belongs at the top level
    metadict['objectid'] = metadict['objectinfo']['objectid'][:]
    del metadict['objectinfo']['objectid']

    # get the lightcurve metadata
    metadatainfo = [x.split(';') for x in metadatainfo]
    for elem in metadatainfo:
        for kvelem in elem:

            try:
                key, val = kvelem.split(' = ',1)

                # get the lcbestaperture into a dict again
                if key.strip() == 'lcbestaperture':
                    val = json.loads(val)

                # get the lcversion and datarelease as integers
                if key.strip() in ('datarelease', 'lcversion'):
                    val = int(val)

                # get the lastupdated as a float
                if key.strip() == 'lastupdated':
                    val = float(val)

                # put the key-val into the dict
                metadict[key.strip()] = val

            except Exception as e:

                LOGWARNING('could not understand header element "%s",'
                           ' skipped.' % kvelem)


    # get the camera filters
    metadict['filters'] = []
    for row in camfilterinfo:
        filterid, filtername, filterdesc = row.split(' - ')
        metadict['filters'].append((int(filterid),
                                    filtername,
                                    filterdesc))

    # get the photometric apertures
    metadict['lcapertures'] = {}
    for row in photapertureinfo:
        apnum, appix = row.split(' - ')
        appix = float(appix.rstrip(' px'))
        metadict['lcapertures'][apnum.strip()] = appix

    # get the columns
    metadict['columns'] = []

    for row in columninfo:
        colnum, colname, coldesc = row.split(' - ')
        metadict['columns'].append(colname)

    return metadict