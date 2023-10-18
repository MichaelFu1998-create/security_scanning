def read_k2sff_lightcurve(lcfits):
    '''This reads a K2 SFF (Vandenberg+ 2014) light curve into an `lcdict`.

    Use this with the light curves from the K2 SFF project at MAST.

    Parameters
    ----------

    lcfits : str
        The filename of the FITS light curve file downloaded from MAST.

    Returns
    -------

    lcdict
        Returns an `lcdict` (this is useable by most astrobase functions for LC
        processing).

    '''

    # read the fits file
    hdulist = pyfits.open(lcfits)
    lchdr, lcdata = hdulist[1].header, hdulist[1].data
    lctophdr = hdulist[0].header

    hdulist.close()

    hdrinfo = {}

    # get the number of detections
    ndet = lchdr['NAXIS2']

    # get the info from the topheader
    for key in SFFTOPKEYS:
        if key in lctophdr and lctophdr[key] is not None:
            hdrinfo[key.lower()] = lctophdr[key]
        else:
            hdrinfo[key.lower()] = None

    # now get the values we want from the header
    for key in SFFHEADERKEYS:
        if key in lchdr and lchdr[key] is not None:
            hdrinfo[key.lower()] = lchdr[key]
        else:
            hdrinfo[key.lower()] = None

    # form the lcdict
    # the metadata is one-elem arrays because we might add on to them later
    lcdict = {
        'quarter':[hdrinfo['quarter']],
        'season':[hdrinfo['season']],
        'datarelease':[hdrinfo['data_rel']],
        'obsmode':[hdrinfo['obsmode']],
        'objectid':hdrinfo['object'],
        'campaign':[hdrinfo['campaign']],
        'lcinfo':{
            'timesys':[hdrinfo['timesys']],
            'bjdoffset':[hdrinfo['bjdrefi'] + hdrinfo['bjdreff']],
            'exptime':[hdrinfo['exposure']],
            'lcapermaskidx':[hdrinfo['maskinde']],
            'lcapermasktype':[hdrinfo['masktype']],
            'aperpixused':[hdrinfo['npixsap']],
            'aperpixunused':[None],
            'pixarcsec':[None],
            'channel':[hdrinfo['channel']],
            'skygroup':[hdrinfo['skygroup']],
            'module':[hdrinfo['module']],
            'output':[hdrinfo['output']],
            'ndet':[ndet],
        },
        'objectinfo':{
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
            'aptgttotrat':[hdrinfo['crowdsap']],
            'aptgtfrac':[hdrinfo['flfrcsap']],
        },
    }

    # get the LC columns
    for key in SFFDATAKEYS:
        lcdict[key.lower()] = lcdata[key]

    # add some of the light curve information to the data arrays so we can sort
    # on them later
    lcdict['channel'] = npfull_like(lcdict['t'],
                                    lcdict['lcinfo']['channel'][0])
    lcdict['skygroup'] = npfull_like(lcdict['t'],
                                     lcdict['lcinfo']['skygroup'][0])
    lcdict['module'] = npfull_like(lcdict['t'],
                                   lcdict['lcinfo']['module'][0])
    lcdict['output'] = npfull_like(lcdict['t'],
                                   lcdict['lcinfo']['output'][0])
    lcdict['quarter'] = npfull_like(lcdict['t'],
                                    lcdict['quarter'][0])
    lcdict['season'] = npfull_like(lcdict['t'],
                                   lcdict['season'][0])
    lcdict['campaign'] = npfull_like(lcdict['t'],
                                     lcdict['campaign'][0])

    # update the lcdict columns with the actual columns
    lcdict['columns'] = (
        [x.lower() for x in SFFDATAKEYS] +
        ['channel','skygroup','module','output','quarter','season','campaign']
    )

    # return the lcdict at the end
    return lcdict