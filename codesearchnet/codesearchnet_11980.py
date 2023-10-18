def describe(lcdict, returndesc=False, offsetwith=None):
    '''This describes the light curve object and columns present.

    Parameters
    ----------

    lcdict : dict
        The input lcdict to parse for column and metadata info.

    returndesc : bool
        If True, returns the description string as an str instead of just
        printing it to stdout.

    offsetwith : str
        This is a character to offset the output description lines by. This is
        useful to add comment characters like '#' to the output description
        lines.

    Returns
    -------

    str or None
        If returndesc is True, returns the description lines as a str, otherwise
        returns nothing.

    '''

    # transparently read LCC CSV format description
    if 'lcformat' in lcdict and 'lcc-csv' in lcdict['lcformat'].lower():
        return describe_lcc_csv(lcdict, returndesc=returndesc)


    # figure out the columndefs part of the header string
    columndefs = []

    for colind, column in enumerate(lcdict['columns']):

        if '_' in column:
            colkey, colap = column.split('_')
            coldesc = COLUMNDEFS[colkey][0] % colap
        else:
            coldesc = COLUMNDEFS[column][0]

        columndefstr = '%03i - %s - %s' % (colind,
                                           column,
                                           coldesc)
        columndefs.append(columndefstr)

    columndefs = '\n'.join(columndefs)

    # figure out the filterdefs
    filterdefs = []

    for row in lcdict['filters']:

        filterid, filtername, filterdesc = row
        filterdefstr = '%s - %s - %s' % (filterid,
                                         filtername,
                                         filterdesc)
        filterdefs.append(filterdefstr)

    filterdefs = '\n'.join(filterdefs)


    # figure out the apertures
    aperturedefs = []
    for key in sorted(lcdict['lcapertures'].keys()):
        aperturedefstr = '%s - %.2f px' % (key, lcdict['lcapertures'][key])
        aperturedefs.append(aperturedefstr)

    aperturedefs = '\n'.join(aperturedefs)

    # now fill in the description
    description = DESCTEMPLATE.format(
        objectid=lcdict['objectid'],
        hatid=lcdict['objectinfo']['hatid'],
        twomassid=lcdict['objectinfo']['twomassid'].strip(),
        ra=lcdict['objectinfo']['ra'],
        decl=lcdict['objectinfo']['decl'],
        pmra=lcdict['objectinfo']['pmra'],
        pmra_err=lcdict['objectinfo']['pmra_err'],
        pmdecl=lcdict['objectinfo']['pmdecl'],
        pmdecl_err=lcdict['objectinfo']['pmdecl_err'],
        jmag=lcdict['objectinfo']['jmag'],
        hmag=lcdict['objectinfo']['hmag'],
        kmag=lcdict['objectinfo']['kmag'],
        bmag=lcdict['objectinfo']['bmag'],
        vmag=lcdict['objectinfo']['vmag'],
        sdssg=lcdict['objectinfo']['sdssg'],
        sdssr=lcdict['objectinfo']['sdssr'],
        sdssi=lcdict['objectinfo']['sdssi'],
        ndet=lcdict['objectinfo']['ndet'],
        lcsortcol=lcdict['lcsortcol'],
        lcbestaperture=json.dumps(lcdict['lcbestaperture'],ensure_ascii=True),
        network=lcdict['objectinfo']['network'],
        stations=lcdict['objectinfo']['stations'],
        lastupdated=lcdict['lastupdated'],
        datarelease=lcdict['datarelease'],
        lcversion=lcdict['lcversion'],
        lcserver=lcdict['lcserver'],
        comment=lcdict['comment'],
        lcfiltersql=(lcdict['lcfiltersql'] if 'lcfiltersql' in lcdict else ''),
        lcnormcols=(lcdict['lcnormcols'] if 'lcnormcols' in lcdict else ''),
        filterdefs=filterdefs,
        columndefs=columndefs,
        aperturedefs=aperturedefs
    )

    if offsetwith is not None:
        description = textwrap.indent(
            description,
            '%s ' % offsetwith,
            lambda line: True
        )
        print(description)
    else:
        print(description)

    if returndesc:
        return description