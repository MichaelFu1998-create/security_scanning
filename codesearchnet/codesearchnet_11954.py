def consolidate_tess_fitslc(lclist,
                            normalize=True,
                            filterqualityflags=False,
                            nanfilter=None,
                            timestoignore=None,
                            headerkeys=LCHEADERKEYS,
                            datakeys=LCDATAKEYS,
                            sapkeys=LCSAPKEYS,
                            pdckeys=LCPDCKEYS,
                            topkeys=LCTOPKEYS,
                            apkeys=LCAPERTUREKEYS):
    '''This consolidates a list of LCs for a single TIC object.

    NOTE: if light curve time arrays contain nans, these and their associated
    measurements will be sorted to the end of the final combined arrays.

    Parameters
    ----------

    lclist : list of str, or str
        `lclist` is either a list of actual light curve files or a string that
        is valid for glob.glob to search for and generate a light curve list
        based on the file glob. This is useful for consolidating LC FITS files
        across different TESS sectors for a single TIC ID using a glob like
        `*<TICID>*_lc.fits`.

    normalize : bool
        If True, then the light curve's SAP_FLUX and PDCSAP_FLUX measurements
        will be normalized to 1.0 by dividing out the median flux for the
        component light curve.

    filterqualityflags : bool
        If True, will remove any measurements that have non-zero quality flags
        present. This usually indicates an issue with the instrument or
        spacecraft.

    nanfilter : {'sap','pdc','sap,pdc'} or None
        Indicates the flux measurement type(s) to apply the filtering to.

    timestoignore : list of tuples or None
        This is of the form::

            [(time1_start, time1_end), (time2_start, time2_end), ...]

        and indicates the start and end times to mask out of the final
        lcdict. Use this to remove anything that wasn't caught by the quality
        flags.

    headerkeys : list
        A list of FITS header keys that will be extracted from the FITS light
        curve file. These describe the observations. The default value for this
        is given in `LCHEADERKEYS` above.

    datakeys : list
        A list of FITS column names that correspond to the auxiliary
        measurements in the light curve. The default is `LCDATAKEYS` above.

    sapkeys : list
        A list of FITS column names that correspond to the SAP flux
        measurements in the light curve. The default is `LCSAPKEYS` above.

    pdckeys : list
        A list of FITS column names that correspond to the PDC flux
        measurements in the light curve. The default is `LCPDCKEYS` above.

    topkeys : list
        A list of FITS header keys that describe the object in the light
        curve. The default is `LCTOPKEYS` above.

    apkeys : list
        A list of FITS header keys that describe the flux measurement apertures
        used by the TESS pipeline. The default is `LCAPERTUREKEYS` above.

    Returns
    -------

    lcdict
        Returns an `lcdict` (this is useable by most astrobase functions for LC
        processing).

    '''

    # if the lclist is a string, assume that we're passing in a fileglob
    if isinstance(lclist, str):

        if sys.version_info[:2] > (3,4):

            matching = glob.glob(lclist,
                                 recursive=True)
            LOGINFO('found %s LCs: %r' % (len(matching), matching))

        else:

            lcfitsdir = os.path.dirname(lclist)
            lcfitsfile = os.path.basename(lclist)
            walker = os.walk(lcfitsdir)
            matching = []
            for root, dirs, _files in walker:
                for sdir in dirs:
                    searchpath = os.path.join(root,
                                              sdir,
                                              lcfitsfile)
                    foundfiles = glob.glob(searchpath)

                    if foundfiles:
                        matching.extend(foundfiles)
                        LOGINFO(
                            'found %s in dir: %s' % (repr(foundfiles),
                                                     os.path.join(root,sdir))
                        )


        if len(matching) == 0:
            LOGERROR('could not find any TESS LC files matching glob: %s' %
                     lclist)
            return None

    # if the lclist is an actual list of LCs, then use it directly
    else:

        matching = lclist

    # get the first file
    consolidated = read_tess_fitslc(matching[0],
                                    normalize=normalize,
                                    headerkeys=LCHEADERKEYS,
                                    datakeys=LCDATAKEYS,
                                    sapkeys=LCSAPKEYS,
                                    pdckeys=LCPDCKEYS,
                                    topkeys=LCTOPKEYS,
                                    apkeys=LCAPERTUREKEYS)

    # get the rest of the files
    if len(matching) > 1:

        for lcf in matching[1:]:

            consolidated = read_tess_fitslc(lcf,
                                            appendto=consolidated,
                                            normalize=normalize,
                                            headerkeys=LCHEADERKEYS,
                                            datakeys=LCDATAKEYS,
                                            sapkeys=LCSAPKEYS,
                                            pdckeys=LCPDCKEYS,
                                            topkeys=LCTOPKEYS,
                                            apkeys=LCAPERTUREKEYS)


    # get the sort indices. we use time for the columns and sectors for the
    # bits in lcinfo and varinfo
    LOGINFO('sorting by time...')

    # NOTE: nans in time will be sorted to the end of the array
    finiteind = np.isfinite(consolidated['time'])
    if np.sum(finiteind) < consolidated['time'].size:
        LOGWARNING('some time values are nan! '
                   'measurements at these times will be '
                   'sorted to the end of the column arrays.')

    # get the time sort index
    column_sort_ind = np.argsort(consolidated['time'])

    # sort the columns by time
    for col in consolidated['columns']:
        if '.' in col:
            key, subkey = col.split('.')
            consolidated[key][subkey] = (
                consolidated[key][subkey][column_sort_ind]
            )
        else:
            consolidated[col] = consolidated[col][column_sort_ind]


    info_sort_ind = np.argsort(consolidated['lcinfo']['sector'])

    # sort the keys in lcinfo
    for key in consolidated['lcinfo']:
        consolidated['lcinfo'][key] = (
            np.array(consolidated['lcinfo'][key])[info_sort_ind].tolist()
        )

    # sort the keys in varinfo
    for key in consolidated['varinfo']:
        consolidated['varinfo'][key] = (
            np.array(consolidated['varinfo'][key])[info_sort_ind].tolist()
        )


    # filter the LC dict if requested
    # we do this at the end
    if (filterqualityflags is not False or
        nanfilter is not None or
        timestoignore is not None):
        consolidated = filter_tess_lcdict(consolidated,
                                          filterqualityflags,
                                          nanfilter=nanfilter,
                                          timestoignore=timestoignore)

    return consolidated