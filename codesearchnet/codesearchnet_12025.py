def _parse_xmatch_catalog_header(xc, xk):
    '''
    This parses the header for a catalog file and returns it as a file object.

    Parameters
    ----------

    xc : str
        The file name of an xmatch catalog prepared previously.

    xk : list of str
        This is a list of column names to extract from the xmatch catalog.

    Returns
    -------

    tuple
        The tuple returned is of the form::

            (infd: the file object associated with the opened xmatch catalog,
             catdefdict: a dict describing the catalog column definitions,
             catcolinds: column number indices of the catalog,
             catcoldtypes: the numpy dtypes of the catalog columns,
             catcolnames: the names of each catalog column,
             catcolunits: the units associated with each catalog column)

    '''

    catdef = []

    # read in this catalog and transparently handle gzipped files
    if xc.endswith('.gz'):
        infd = gzip.open(xc,'rb')
    else:
        infd = open(xc,'rb')

    # read in the defs
    for line in infd:
        if line.decode().startswith('#'):
            catdef.append(
                line.decode().replace('#','').strip().rstrip('\n')
            )
        if not line.decode().startswith('#'):
            break

    if not len(catdef) > 0:
        LOGERROR("catalog definition not parseable "
                 "for catalog: %s, skipping..." % xc)
        return None

    catdef = ' '.join(catdef)
    catdefdict = json.loads(catdef)

    catdefkeys = [x['key'] for x in catdefdict['columns']]
    catdefdtypes = [x['dtype'] for x in catdefdict['columns']]
    catdefnames = [x['name'] for x in catdefdict['columns']]
    catdefunits = [x['unit'] for x in catdefdict['columns']]

    # get the correct column indices and dtypes for the requested columns
    # from the catdefdict

    catcolinds = []
    catcoldtypes = []
    catcolnames = []
    catcolunits = []

    for xkcol in xk:

        if xkcol in catdefkeys:

            xkcolind = catdefkeys.index(xkcol)

            catcolinds.append(xkcolind)
            catcoldtypes.append(catdefdtypes[xkcolind])
            catcolnames.append(catdefnames[xkcolind])
            catcolunits.append(catdefunits[xkcolind])


    return (infd, catdefdict,
            catcolinds, catcoldtypes, catcolnames, catcolunits)