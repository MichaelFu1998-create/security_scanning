def consolidate_kepler_fitslc(keplerid,
                              lcfitsdir,
                              normalize=True,
                              headerkeys=LCHEADERKEYS,
                              datakeys=LCDATAKEYS,
                              sapkeys=LCSAPKEYS,
                              pdckeys=LCPDCKEYS,
                              topkeys=LCTOPKEYS,
                              apkeys=LCAPERTUREKEYS):
    '''This gets all Kepler/K2 light curves for the given `keplerid`
    in `lcfitsdir`.

    Searches recursively in `lcfitsdir` for all of the files belonging to the
    specified `keplerid`. Sorts the light curves by time. Returns an
    `lcdict`. This is meant to be used to consolidate light curves for a single
    object across Kepler quarters.

    NOTE: `keplerid` is an integer (without the leading zeros). This is usually
    the KIC ID.

    NOTE: if light curve time arrays contain `nans`, these and their associated
    measurements will be sorted to the end of the final combined arrays.

    Parameters
    ----------

    keplerid : int
        The Kepler ID of the object to consolidate LCs for, as an integer
        without any leading zeros. This is usually the KIC or EPIC ID.

    lcfitsdir : str
        The directory to look in for LCs of the specified object.

    normalize : bool
        If True, then each component light curve's SAP_FLUX and PDCSAP_FLUX
        measurements will be normalized to 1.0 by dividing out the median flux
        for the component light curve.

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
        used by the Kepler/K2 pipeline. The default is `LCAPERTUREKEYS` above.

    Returns
    -------

    lcdict
        Returns an `lcdict` (this is useable by most astrobase functions for LC
        processing).

    '''

    LOGINFO('looking for Kepler light curve FITS in %s for %s...' % (lcfitsdir,
                                                                     keplerid))

    # for Python 3.5 and up, use recursive glob, it appears to be absurdly
    # faster than os.walk
    if sys.version_info[:2] > (3,4):

        matching = glob.glob(os.path.join(lcfitsdir,
                                          '**',
                                          'kplr%09i-*_llc.fits' % keplerid),
                             recursive=True)
        LOGINFO('found %s files: %s' % (len(matching), repr(matching)))

    # for Python < 3.5, use os.walk and glob
    else:

        # use the os.walk function to start looking for files in lcfitsdir
        walker = os.walk(lcfitsdir)
        matching = []
        for root, dirs, _files in walker:
            for sdir in dirs:
                searchpath = os.path.join(root,
                                          sdir,
                                          'kplr%09i-*_llc.fits' % keplerid)
                foundfiles = glob.glob(searchpath)

                if foundfiles:
                    matching.extend(foundfiles)
                    LOGINFO('found %s in dir: %s' % (repr(foundfiles),
                                                     os.path.join(root,sdir)))

    # now that we've found everything, read them all in
    if len(matching) > 0:

        LOGINFO('consolidating...')

        # the first file
        consolidated = read_kepler_fitslc(matching[0],
                                          headerkeys=headerkeys,
                                          datakeys=datakeys,
                                          sapkeys=sapkeys,
                                          pdckeys=pdckeys,
                                          topkeys=topkeys,
                                          apkeys=apkeys,
                                          normalize=normalize)


        # get the rest of the files
        for lcf in matching:
            consolidated = read_kepler_fitslc(lcf,
                                              appendto=consolidated,
                                              headerkeys=headerkeys,
                                              datakeys=datakeys,
                                              sapkeys=sapkeys,
                                              pdckeys=pdckeys,
                                              topkeys=topkeys,
                                              apkeys=apkeys,
                                              normalize=normalize)

        # get the sort indices
        # we use time for the columns and quarters for the headers
        LOGINFO('sorting by time...')

        # NOTE: nans in time will be sorted to the end of the array
        finiteind = npisfinite(consolidated['time'])
        if npsum(finiteind) < consolidated['time'].size:
            LOGWARNING('some time values are nan! '
                       'measurements at these times will be '
                       'sorted to the end of the column arrays.')

        # get the sort index
        column_sort_ind = npargsort(consolidated['time'])

        # sort the columns by time
        for col in consolidated['columns']:
            if '.' in col:
                key, subkey = col.split('.')
                consolidated[key][subkey] = (
                    consolidated[key][subkey][column_sort_ind]
                )
            else:
                consolidated[col] = consolidated[col][column_sort_ind]

        # now sort the headers by quarters
        header_sort_ind = npargsort(consolidated['quarter']).tolist()

        # this is a bit convoluted, but whatever: list -> array -> list

        for key in ('quarter', 'season', 'datarelease', 'obsmode'):
            consolidated[key] = (
                nparray(consolidated[key])[header_sort_ind].tolist()
            )

        for key in ('timesys','bjdoffset','exptime','lcaperture',
                    'aperpixused','aperpixunused','pixarcsec',
                    'channel','skygroup','module','output','ndet'):
            consolidated['lcinfo'][key] = (
                nparray(consolidated['lcinfo'][key])[header_sort_ind].tolist()
            )

        for key in ('cdpp3_0','cdpp6_0','cdpp12_0','pdcvar','pdcmethod',
                    'aper_target_total_ratio','aper_target_frac'):
            consolidated['varinfo'][key] = (
                nparray(consolidated['varinfo'][key])[header_sort_ind].tolist()
            )

        # finally, return the consolidated lcdict
        return consolidated

    # if we didn't find anything, complain
    else:

        LOGERROR('could not find any light curves '
                 'for %s in %s or its subdirectories' % (keplerid,
                                                         lcfitsdir))
        return None