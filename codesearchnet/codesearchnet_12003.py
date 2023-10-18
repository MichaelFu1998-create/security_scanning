def _parse_csv_header(header):
    '''This parses a CSV header from a K2 CSV LC.

    Returns a dict that can be used to update an existing lcdict with the
    relevant metadata info needed to form a full LC.

    '''

    # first, break into lines
    headerlines = header.split('\n')
    headerlines = [x.lstrip('# ') for x in headerlines]

    # next, find the indices of the '# COLUMNS' line and '# LIGHTCURVE' line
    metadatastart = headerlines.index('METADATA')
    columnstart = headerlines.index('COLUMNS')
    lcstart = headerlines.index('LIGHTCURVE')

    # get the lines for the metadata and columndefs
    metadata = headerlines[metadatastart+1:columnstart-1]
    columndefs = headerlines[columnstart+1:lcstart-1]

    # parse the metadata
    metainfo = [x.split(',') for x in metadata][:-1]
    aperpixradius = metadata[-1]

    objectid, kepid, ucac4id, kepmag = metainfo[0]
    objectid, kepid, ucac4id, kepmag = (objectid.split(' = ')[-1],
                                        kepid.split(' = ')[-1],
                                        ucac4id.split(' = ')[-1],
                                        kepmag.split(' = ')[-1])
    kepmag = float(kepmag) if kepmag else None

    ra, decl, ndet, k2campaign = metainfo[1]
    ra, decl, ndet, k2campaign = (ra.split(' = ')[-1],
                                  decl.split(' = ')[-1],
                                  int(ndet.split(' = ')[-1]),
                                  int(k2campaign.split(' = ')[-1]))

    fovccd, fovchannel, fovmodule = metainfo[2]
    fovccd, fovchannel, fovmodule = (int(fovccd.split(' = ')[-1]),
                                     int(fovchannel.split(' = ')[-1]),
                                     int(fovmodule.split(' = ')[-1]))

    try:
        qualflag, bjdoffset, napertures = metainfo[3]
        qualflag, bjdoffset, napertures = (int(qualflag.split(' = ')[-1]),
                                           float(bjdoffset.split(' = ')[-1]),
                                           int(napertures.split(' = ')[-1]))
        kernelspec = None
    except Exception as e:
        qualflag, bjdoffset, napertures, kernelspec = metainfo[3]
        qualflag, bjdoffset, napertures, kernelspec = (
            int(qualflag.split(' = ')[-1]),
            float(bjdoffset.split(' = ')[-1]),
            int(napertures.split(' = ')[-1]),
            str(kernelspec.split(' = ')[-1])
        )

    aperpixradius = aperpixradius.split(' = ')[-1].split(',')
    aperpixradius = [float(x) for x in aperpixradius]

    # parse the columndefs
    columns = [x.split(' - ')[1] for x in columndefs]

    metadict = {'objectid':objectid,
                'objectinfo':{
                    'objectid':objectid,
                    'kepid':kepid,
                    'ucac4id':ucac4id,
                    'kepmag':kepmag,
                    'ra':ra,
                    'decl':decl,
                    'ndet':ndet,
                    'k2campaign':k2campaign,
                    'fovccd':fovccd,
                    'fovchannel':fovchannel,
                    'fovmodule':fovmodule,
                    'qualflag':qualflag,
                    'bjdoffset':bjdoffset,
                    'napertures':napertures,
                    'kernelspec':kernelspec,
                    'aperpixradius':aperpixradius,
                },
                'columns':columns}

    return metadict