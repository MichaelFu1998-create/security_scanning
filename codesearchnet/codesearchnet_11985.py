def describe_lcc_csv(lcdict, returndesc=False):
    '''
    This describes the LCC CSV format light curve file.

    Parameters
    ----------

    lcdict : dict
        The input lcdict to parse for column and metadata info.

    returndesc : bool
        If True, returns the description string as an str instead of just
        printing it to stdout.

    Returns
    -------

    str or None
        If returndesc is True, returns the description lines as a str, otherwise
        returns nothing.

    '''

    metadata_lines = []
    coldef_lines = []

    if 'lcformat' in lcdict and 'lcc-csv' in lcdict['lcformat'].lower():

        metadata = lcdict['metadata']
        metakeys = lcdict['objectinfo'].keys()
        coldefs = lcdict['coldefs']

        for mk in metakeys:

            metadata_lines.append(
                '%20s | %s' % (
                    mk,
                    metadata[mk]['desc']
                )
            )

        for ck in lcdict['columns']:

            coldef_lines.append('column %02d | %8s | numpy dtype: %3s | %s'
                                % (coldefs[ck]['colnum'],
                                   ck,
                                   coldefs[ck]['dtype'],
                                   coldefs[ck]['desc']))




        desc = LCC_CSVLC_DESCTEMPLATE.format(
            objectid=lcdict['objectid'],
            metadata_desc='\n'.join(metadata_lines),
            metadata=pformat(lcdict['objectinfo']),
            columndefs='\n'.join(coldef_lines)
        )

        print(desc)

        if returndesc:
            return desc

    else:
        LOGERROR("this lcdict is not from an LCC CSV, can't figure it out...")
        return None