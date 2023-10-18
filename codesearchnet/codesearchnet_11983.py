def _parse_csv_header_lcc_csv_v1(headerlines):
    '''
    This parses the header of the LCC CSV V1 LC format.

    '''

    # the first three lines indicate the format name, comment char, separator
    commentchar = headerlines[1]
    separator = headerlines[2]

    headerlines = [x.lstrip('%s ' % commentchar) for x in headerlines[3:]]

    # next, find the indices of the various LC sections
    metadatastart = headerlines.index('OBJECT METADATA')
    columnstart = headerlines.index('COLUMN DEFINITIONS')
    lcstart = headerlines.index('LIGHTCURVE')

    metadata = ' ' .join(headerlines[metadatastart+1:columnstart-1])
    columns = ' ' .join(headerlines[columnstart+1:lcstart-1])
    metadata = json.loads(metadata)
    columns = json.loads(columns)

    return metadata, columns, separator