def read_kepler_fitslc(
        lcfits,
        headerkeys=LCHEADERKEYS,
        datakeys=LCDATAKEYS,
        sapkeys=LCSAPKEYS,
        pdckeys=LCPDCKEYS,
        topkeys=LCTOPKEYS,
        apkeys=LCAPERTUREKEYS,
        appendto=None,
        normalize=False,
):
    '''This extracts the light curve from a single Kepler or K2 LC FITS file.

    This works on the light curves available at MAST:

    - `kplr{kepid}-{somedatething}_llc.fits` files from the Kepler mission
    - `ktwo{epicid}-c{campaign}_llc.fits` files from the K2 mission

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
        used by the Kepler/K2 pipeline. The default is `LCAPERTUREKEYS` above.

    appendto : lcdict or None
        If appendto is an `lcdict`, will append measurements of this `lcdict` to
        that `lcdict`. This is used for consolidating light curves for the same
        object across different files (quarters). The appending does not care
        about the time order. To consolidate light curves in time order, use
        `consolidate_kepler_fitslc` below.

    normalize : bool
        If True, then each component light curve's SAP_FLUX and PDCSAP_FLUX
        measurements will be normalized to 1.0 by dividing out the median flux
        for the component light curve.

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

        lcdict['quarter'].append(hdrinfo['quarter'])
        lcdict['season'].append(hdrinfo['season'])
        lcdict['datarelease'].append(hdrinfo['data_rel'])
        lcdict['obsmode'].append(hdrinfo['obsmode'])
        lcdict['campaign'].append(hdrinfo['campaign'])
        # we don't update the objectid

        # update lcinfo
        lcdict['lcinfo']['timesys'].append(hdrinfo['timesys'])
        lcdict['lcinfo']['bjdoffset'].append(
            hdrinfo['bjdrefi'] + hdrinfo['bjdreff']
        )
        lcdict['lcinfo']['exptime'].append(hdrinfo['exposure'])
        lcdict['lcinfo']['lcaperture'].append(lcaperturedata)
        lcdict['lcinfo']['aperpixused'].append(hdrinfo['npixsap'])
        lcdict['lcinfo']['aperpixunused'].append(hdrinfo['npixmiss'])
        lcdict['lcinfo']['pixarcsec'].append(
            (npabs(hdrinfo['cdelt1']) +
             npabs(hdrinfo['cdelt2']))*3600.0/2.0
        )
        lcdict['lcinfo']['channel'].append(hdrinfo['channel'])
        lcdict['lcinfo']['skygroup'].append(hdrinfo['skygroup'])
        lcdict['lcinfo']['module'].append(hdrinfo['module'])
        lcdict['lcinfo']['output'].append(hdrinfo['output'])
        lcdict['lcinfo']['ndet'].append(ndet)

        # the objectinfo is not updated for the same object when appending to a
        # light curve. FIXME: maybe it should be?

        # update the varinfo for this light curve
        lcdict['varinfo']['cdpp3_0'].append(hdrinfo['cdpp3_0'])
        lcdict['varinfo']['cdpp6_0'].append(hdrinfo['cdpp6_0'])
        lcdict['varinfo']['cdpp12_0'].append(hdrinfo['cdpp12_0'])
        lcdict['varinfo']['pdcvar'].append(hdrinfo['pdcvar'])
        lcdict['varinfo']['pdcmethod'].append(hdrinfo['pdcmethd'])
        lcdict['varinfo']['aper_target_total_ratio'].append(hdrinfo['crowdsap'])
        lcdict['varinfo']['aper_target_frac'].append(hdrinfo['flfrcsap'])

        # update the light curve columns now
        for key in datakeys:
            if key.lower() in lcdict:
                lcdict[key.lower()] = (
                    npconcatenate((lcdict[key.lower()], lcdata[key]))
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
        lcdict['lc_channel'] = npconcatenate(
            (lcdict['lc_channel'],
             npfull_like(lcdata['TIME'],
                         hdrinfo['channel']))
        )
        lcdict['lc_skygroup'] = npconcatenate(
            (lcdict['lc_skygroup'],
             npfull_like(lcdata['TIME'],
                         hdrinfo['skygroup']))
        )
        lcdict['lc_module'] = npconcatenate(
            (lcdict['lc_module'],
             npfull_like(lcdata['TIME'],
                         hdrinfo['module']))
        )
        lcdict['lc_output'] = npconcatenate(
            (lcdict['lc_output'],
             npfull_like(lcdata['TIME'],
                         hdrinfo['output']))
        )
        lcdict['lc_quarter'] = npconcatenate(
            (lcdict['lc_quarter'],
             npfull_like(lcdata['TIME'],
                         hdrinfo['quarter']))
        )
        lcdict['lc_season'] = npconcatenate(
            (lcdict['lc_season'],
             npfull_like(lcdata['TIME'],
                         hdrinfo['season']))
        )
        lcdict['lc_campaign'] = npconcatenate(
            (lcdict['lc_campaign'],
             npfull_like(lcdata['TIME'],
                         hdrinfo['campaign']))
        )


    # otherwise, this is a new lcdict
    else:

        # form the lcdict
        # the metadata is one-elem arrays because we might add on to them later
        lcdict = {
            'quarter':[hdrinfo['quarter']],
            'season':[hdrinfo['season']],
            'datarelease':[hdrinfo['data_rel']],
            'campaign':[hdrinfo['campaign']],  # this is None for KepPrime
            'obsmode':[hdrinfo['obsmode']],
            'objectid':hdrinfo['object'],
            'lcinfo':{
                'timesys':[hdrinfo['timesys']],
                'bjdoffset':[hdrinfo['bjdrefi'] + hdrinfo['bjdreff']],
                'exptime':[hdrinfo['exposure']],
                'lcaperture':[lcaperturedata],
                'aperpixused':[hdrinfo['npixsap']],
                'aperpixunused':[hdrinfo['npixmiss']],
                'pixarcsec':[(npabs(hdrinfo['cdelt1']) +
                             npabs(hdrinfo['cdelt2']))*3600.0/2.0],
                'channel':[hdrinfo['channel']],
                'skygroup':[hdrinfo['skygroup']],
                'module':[hdrinfo['module']],
                'output':[hdrinfo['output']],
                'ndet':[ndet],
            },
            'objectinfo':{
                'objectid':hdrinfo['object'],  # repeated here for checkplot use
                'keplerid':hdrinfo['keplerid'],
                'ra':hdrinfo['ra_obj'],
                'decl':hdrinfo['dec_obj'],
                'pmra':hdrinfo['pmra'],
                'pmdecl':hdrinfo['pmdec'],
                'pmtotal':hdrinfo['pmtotal'],
                'sdssg':hdrinfo['gmag'],
                'sdssr':hdrinfo['rmag'],
                'sdssi':hdrinfo['imag'],
                'sdssz':hdrinfo['zmag'],
                'kepmag':hdrinfo['kepmag'],
                'teff':hdrinfo['teff'],
                'logg':hdrinfo['logg'],
                'feh':hdrinfo['feh'],
                'ebminusv':hdrinfo['ebminusv'],
                'extinction':hdrinfo['av'],
                'starradius':hdrinfo['radius'],
                'twomassuid':hdrinfo['tmindex'],
            },
            'varinfo':{
                'cdpp3_0':[hdrinfo['cdpp3_0']],
                'cdpp6_0':[hdrinfo['cdpp6_0']],
                'cdpp12_0':[hdrinfo['cdpp12_0']],
                'pdcvar':[hdrinfo['pdcvar']],
                'pdcmethod':[hdrinfo['pdcmethd']],
                'aper_target_total_ratio':[hdrinfo['crowdsap']],
                'aper_target_frac':[hdrinfo['flfrcsap']],
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
        lcdict['lc_channel'] = npfull_like(lcdict['time'],
                                           lcdict['lcinfo']['channel'][0])
        lcdict['lc_skygroup'] = npfull_like(lcdict['time'],
                                            lcdict['lcinfo']['skygroup'][0])
        lcdict['lc_module'] = npfull_like(lcdict['time'],
                                          lcdict['lcinfo']['module'][0])
        lcdict['lc_output'] = npfull_like(lcdict['time'],
                                          lcdict['lcinfo']['output'][0])
        lcdict['lc_quarter'] = npfull_like(lcdict['time'],
                                           lcdict['quarter'][0])
        lcdict['lc_season'] = npfull_like(lcdict['time'],
                                          lcdict['season'][0])
        lcdict['lc_campaign'] = npfull_like(lcdict['time'],
                                            lcdict['campaign'][0])

        # normalize the SAP and PDCSAP fluxes if needed
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
        ['lc_channel','lc_skygroup','lc_module',
         'lc_output','lc_quarter','lc_season']
    )

    # return the lcdict at the end
    return lcdict