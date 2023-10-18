def read_tess_fitslc(lcfits,
                     headerkeys=LCHEADERKEYS,
                     datakeys=LCDATAKEYS,
                     sapkeys=LCSAPKEYS,
                     pdckeys=LCPDCKEYS,
                     topkeys=LCTOPKEYS,
                     apkeys=LCAPERTUREKEYS,
                     normalize=False,
                     appendto=None,
                     filterqualityflags=False,
                     nanfilter=None,
                     timestoignore=None):
    '''This extracts the light curve from a single TESS .lc.fits file.

    This works on the light curves available at MAST.

    TODO: look at:

    https://archive.stsci.edu/missions/tess/doc/EXP-TESS-ARC-ICD-TM-0014.pdf

    for details on the column descriptions and to fill in any other info we
    need.

    Parameters
    ----------

    lcfits : str
        The filename of a MAST Kepler/K2 light curve FITS file.

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

    normalize : bool
        If True, then the light curve's SAP_FLUX and PDCSAP_FLUX measurements
        will be normalized to 1.0 by dividing out the median flux for the
        component light curve.

    appendto : lcdict or None
        If appendto is an `lcdict`, will append measurements of this `lcdict` to
        that `lcdict`. This is used for consolidating light curves for the same
        object across different files (sectors/cameras/CCDs?). The appending
        does not care about the time order. To consolidate light curves in time
        order, use `consolidate_tess_fitslc` below.

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

    Returns
    -------

    lcdict
        Returns an `lcdict` (this is useable by most astrobase functions for LC
        processing).

    '''

    # read the fits file
    hdulist = pyfits.open(lcfits)
    lchdr, lcdata = hdulist[1].header, hdulist[1].data
    lctophdr, lcaperturehdr, lcaperturedata = (hdulist[0].header,
                                               hdulist[2].header,
                                               hdulist[2].data)
    hdulist.close()

    hdrinfo = {}

    # now get the values we want from the header
    for key in headerkeys:
        if key in lchdr and lchdr[key] is not None:
            hdrinfo[key.lower()] = lchdr[key]
        else:
            hdrinfo[key.lower()] = None

    # get the number of detections
    ndet = lchdr['NAXIS2']

    # get the info from the topheader
    for key in topkeys:
        if key in lctophdr and lctophdr[key] is not None:
            hdrinfo[key.lower()] = lctophdr[key]
        else:
            hdrinfo[key.lower()] = None

    # get the info from the lcaperturehdr
    for key in lcaperturehdr:
        if key in lcaperturehdr and lcaperturehdr[key] is not None:
            hdrinfo[key.lower()] = lcaperturehdr[key]
        else:
            hdrinfo[key.lower()] = None


    # if we're appending to another lcdict
    if appendto and isinstance(appendto, dict):

        lcdict = appendto

        # update lcinfo
        lcdict['lcinfo']['timesys'].append(hdrinfo['timesys'])
        lcdict['lcinfo']['bjdoffset'].append(
            hdrinfo['bjdrefi'] + hdrinfo['bjdreff']
        )
        lcdict['lcinfo']['lcaperture'].append(lcaperturedata)
        lcdict['lcinfo']['aperpix_used'].append(hdrinfo['npixsap'])
        lcdict['lcinfo']['aperpix_unused'].append(hdrinfo['npixmiss'])
        lcdict['lcinfo']['pixarcsec'].append(
            (np.abs(hdrinfo['cdelt1']) +
             np.abs(hdrinfo['cdelt2']))*3600.0/2.0
        )
        lcdict['lcinfo']['ndet'].append(ndet)
        lcdict['lcinfo']['exptime'].append(hdrinfo['exposure'])
        lcdict['lcinfo']['sector'].append(hdrinfo['sector'])
        lcdict['lcinfo']['camera'].append(hdrinfo['camera'])
        lcdict['lcinfo']['ccd'].append(hdrinfo['ccd'])

        lcdict['lcinfo']['date_obs_start'].append(hdrinfo['date-obs'])
        lcdict['lcinfo']['date_obs_end'].append(hdrinfo['date-end'])
        lcdict['lcinfo']['pixel_table_id'].append(hdrinfo['pxtable'])
        lcdict['lcinfo']['origin'].append(hdrinfo['origin'])
        lcdict['lcinfo']['datarelease'].append(hdrinfo['data_rel'])
        lcdict['lcinfo']['procversion'].append(hdrinfo['procver'])


        lcdict['lcinfo']['tic_version'].append(hdrinfo['ticver'])
        lcdict['lcinfo']['cr_mitigation'].append(hdrinfo['crmiten'])
        lcdict['lcinfo']['cr_blocksize'].append(hdrinfo['crblksz'])
        lcdict['lcinfo']['cr_spocclean'].append(hdrinfo['crspoc'])

        # update the varinfo for this light curve
        lcdict['varinfo']['cdpp0_5'].append(hdrinfo['cdpp0_5'])
        lcdict['varinfo']['cdpp1_0'].append(hdrinfo['cdpp1_0'])
        lcdict['varinfo']['cdpp2_0'].append(hdrinfo['cdpp2_0'])
        lcdict['varinfo']['pdcvar'].append(hdrinfo['pdcvar'])
        lcdict['varinfo']['pdcmethod'].append(hdrinfo['pdcmethd'])
        lcdict['varinfo']['target_flux_total_flux_ratio_in_aper'].append(
            hdrinfo['crowdsap']
        )
        lcdict['varinfo']['target_flux_fraction_in_aper'].append(
            hdrinfo['flfrcsap']
        )

        # update the light curve columns now
        for key in datakeys:

            if key.lower() in lcdict:
                lcdict[key.lower()] = (
                    np.concatenate((lcdict[key.lower()], lcdata[key]))
                )

        for key in sapkeys:

            if key.lower() in lcdict['sap']:

                sapflux_median = np.nanmedian(lcdata['SAP_FLUX'])

                # normalize the current flux measurements if needed
                if normalize and key == 'SAP_FLUX':
                    thislcdata = lcdata[key] / sapflux_median
                elif normalize and key == 'SAP_FLUX_ERR':
                    thislcdata = lcdata[key] / sapflux_median
                elif normalize and key == 'SAP_BKG':
                    thislcdata = lcdata[key] / sapflux_median
                elif normalize and key == 'SAP_BKG_ERR':
                    thislcdata = lcdata[key] / sapflux_median
                else:
                    thislcdata = lcdata[key]

                lcdict['sap'][key.lower()] = (
                    np.concatenate((lcdict['sap'][key.lower()], thislcdata))
                )

        for key in pdckeys:

            if key.lower() in lcdict['pdc']:

                pdcsap_flux_median = np.nanmedian(lcdata['PDCSAP_FLUX'])

                # normalize the current flux measurements if needed
                if normalize and key == 'PDCSAP_FLUX':
                    thislcdata = lcdata[key] / pdcsap_flux_median
                elif normalize and key == 'PDCSAP_FLUX_ERR':
                    thislcdata = lcdata[key] / pdcsap_flux_median
                else:
                    thislcdata = lcdata[key]

                lcdict['pdc'][key.lower()] = (
                    np.concatenate((lcdict['pdc'][key.lower()], thislcdata))
                )


        # append some of the light curve information into existing numpy arrays
        # so we can sort on them later
        lcdict['exptime'] = np.concatenate(
            (lcdict['exptime'],
             np.full_like(lcdata['TIME'],
                          hdrinfo['exposure'],
                          dtype=np.float64))
        )
        lcdict['sector'] = np.concatenate(
            (lcdict['sector'],
             np.full_like(lcdata['TIME'],
                          hdrinfo['sector'],
                          dtype=np.int64))
        )
        lcdict['camera'] = np.concatenate(
            (lcdict['camera'],
             np.full_like(lcdata['TIME'],
                          hdrinfo['camera'],
                          dtype=np.int64))
        )
        lcdict['ccd'] = np.concatenate(
            (lcdict['ccd'],
             np.full_like(lcdata['TIME'],
                          hdrinfo['ccd'],
                          dtype=np.int64))
        )

        lcdict['pixel_table_id'] = np.concatenate(
            (lcdict['pixel_table_id'],
             np.full_like(lcdata['TIME'],
                          hdrinfo['pxtable'],
                          dtype=np.int64))
        )
        lcdict['origin'] = np.concatenate(
            (lcdict['origin'],
             np.full_like(lcdata['TIME'],
                          hdrinfo['origin'],
                          dtype='U100'))
        )
        lcdict['date_obs_start'] = np.concatenate(
            (lcdict['date_obs_start'],
             np.full_like(lcdata['TIME'],
                          hdrinfo['date-obs'],
                          dtype='U100'))
        )
        lcdict['date_obs_end'] = np.concatenate(
            (lcdict['date_obs_end'],
             np.full_like(lcdata['TIME'],
                          hdrinfo['date-end'],
                          dtype='U100'))
        )
        lcdict['procversion'] = np.concatenate(
            (lcdict['procversion'],
             np.full_like(lcdata['TIME'],
                          hdrinfo['procver'],
                          dtype='U255'))
        )
        lcdict['datarelease'] = np.concatenate(
            (lcdict['datarelease'],
             np.full_like(lcdata['TIME'],
                          hdrinfo['data_rel'],
                          dtype=np.int64))
        )


    # otherwise, this is a new lcdict
    else:

        # form the lcdict
        # the metadata is one-elem arrays because we might add on to them later
        lcdict = {
            'objectid':hdrinfo['object'],
            'lcinfo':{
                'timesys':[hdrinfo['timesys']],
                'bjdoffset':[hdrinfo['bjdrefi'] + hdrinfo['bjdreff']],
                'exptime':[hdrinfo['exposure']],
                'lcaperture':[lcaperturedata],
                'aperpix_used':[hdrinfo['npixsap']],
                'aperpix_unused':[hdrinfo['npixmiss']],
                'pixarcsec':[(np.abs(hdrinfo['cdelt1']) +
                              np.abs(hdrinfo['cdelt2']))*3600.0/2.0],
                'ndet':[ndet],
                'origin':[hdrinfo['origin']],
                'procversion':[hdrinfo['procver']],
                'datarelease':[hdrinfo['data_rel']],
                'sector':[hdrinfo['sector']],
                'camera':[hdrinfo['camera']],
                'ccd':[hdrinfo['ccd']],
                'pixel_table_id':[hdrinfo['pxtable']],
                'date_obs_start':[hdrinfo['date-obs']],
                'date_obs_end':[hdrinfo['date-end']],
                'tic_version':[hdrinfo['ticver']],
                'cr_mitigation':[hdrinfo['crmiten']],
                'cr_blocksize':[hdrinfo['crblksz']],
                'cr_spocclean':[hdrinfo['crspoc']],
            },
            'objectinfo':{
                'objectid':hdrinfo['object'],
                'ticid':hdrinfo['ticid'],
                'tessmag':hdrinfo['tessmag'],
                'ra':hdrinfo['ra_obj'],
                'decl':hdrinfo['dec_obj'],
                'pmra':hdrinfo['pmra'],
                'pmdecl':hdrinfo['pmdec'],
                'pmtotal':hdrinfo['pmtotal'],
                'star_teff':hdrinfo['teff'],
                'star_logg':hdrinfo['logg'],
                'star_mh':hdrinfo['mh'],
                'star_radius':hdrinfo['radius'],
                'observatory':'TESS',
                'telescope':'TESS photometer',
            },
            'varinfo':{
                'cdpp0_5':[hdrinfo['cdpp0_5']],
                'cdpp1_0':[hdrinfo['cdpp1_0']],
                'cdpp2_0':[hdrinfo['cdpp2_0']],
                'pdcvar':[hdrinfo['pdcvar']],
                'pdcmethod':[hdrinfo['pdcmethd']],
                'target_flux_total_flux_ratio_in_aper':[hdrinfo['crowdsap']],
                'target_flux_fraction_in_aper':[hdrinfo['flfrcsap']],
            },
            'sap':{},
            'pdc':{},
        }

        # get the LC columns
        for key in datakeys:
            lcdict[key.lower()] = lcdata[key]
        for key in sapkeys:
            lcdict['sap'][key.lower()] = lcdata[key]
        for key in pdckeys:
            lcdict['pdc'][key.lower()] = lcdata[key]

        # turn some of the light curve information into numpy arrays so we can
        # sort on them later
        lcdict['exptime'] = np.full_like(lcdict['time'],
                                         lcdict['lcinfo']['exptime'][0],
                                         dtype=np.float64)
        lcdict['sector'] = np.full_like(lcdict['time'],
                                        lcdict['lcinfo']['sector'][0],
                                        dtype=np.int64)
        lcdict['camera'] = np.full_like(lcdict['time'],
                                        lcdict['lcinfo']['camera'][0],
                                        dtype=np.int64)
        lcdict['ccd'] = np.full_like(lcdict['time'],
                                     lcdict['lcinfo']['ccd'][0],
                                     dtype=np.int64)

        lcdict['pixel_table_id'] = np.full_like(
            lcdict['time'],
            lcdict['lcinfo']['pixel_table_id'][0],
            dtype=np.int64,
        )
        lcdict['origin'] = np.full_like(
            lcdict['time'],
            lcdict['lcinfo']['origin'][0],
            dtype='U100',
        )
        lcdict['date_obs_start'] = np.full_like(
            lcdict['time'],
            lcdict['lcinfo']['date_obs_start'][0],
            dtype='U100',
        )
        lcdict['date_obs_end'] = np.full_like(
            lcdict['time'],
            lcdict['lcinfo']['date_obs_end'][0],
            dtype='U100',
        )
        lcdict['procversion'] = np.full_like(
            lcdict['time'],
            lcdict['lcinfo']['procversion'][0],
            dtype='U255',
        )
        lcdict['datarelease'] = np.full_like(
            lcdict['time'],
            lcdict['lcinfo']['datarelease'][0],
            dtype=np.int64,
        )


        # normalize the SAP and PDCSAP fluxes, errs, and backgrounds if needed
        if normalize:

            sapflux_median = np.nanmedian(lcdict['sap']['sap_flux'])
            pdcsap_flux_median = np.nanmedian(lcdict['pdc']['pdcsap_flux'])

            lcdict['sap']['sap_flux'] = (
                lcdict['sap']['sap_flux'] /
                sapflux_median
            )
            lcdict['sap']['sap_flux_err'] = (
                lcdict['sap']['sap_flux_err'] /
                sapflux_median
            )

            lcdict['sap']['sap_bkg'] = (
                lcdict['sap']['sap_bkg'] /
                sapflux_median
            )
            lcdict['sap']['sap_bkg_err'] = (
                lcdict['sap']['sap_bkg_err'] /
                sapflux_median
            )

            lcdict['pdc']['pdcsap_flux'] = (
                lcdict['pdc']['pdcsap_flux'] /
                pdcsap_flux_median
            )
            lcdict['pdc']['pdcsap_flux_err'] = (
                lcdict['pdc']['pdcsap_flux_err'] /
                pdcsap_flux_median
            )

    ## END OF LIGHT CURVE CONSTRUCTION ##

    # update the lcdict columns with the actual columns
    lcdict['columns'] = (
        [x.lower() for x in datakeys] +
        ['sap.%s' % x.lower() for x in sapkeys] +
        ['pdc.%s' % x.lower() for x in pdckeys] +
        ['exptime','sector','camera','ccd', 'pixel_table_id',
         'origin', 'date_obs_start', 'date_obs_end',
         'procversion', 'datarelease']
    )

    # update the ndet key in the objectinfo with the sum of all observations
    lcdict['objectinfo']['ndet'] = sum(lcdict['lcinfo']['ndet'])

    # filter the LC dict if requested
    if (filterqualityflags is not False or
        nanfilter is not None or
        timestoignore is not None):
        lcdict = filter_tess_lcdict(lcdict,
                                    filterqualityflags,
                                    nanfilter=nanfilter,
                                    timestoignore=timestoignore)

    # return the lcdict at the end
    return lcdict