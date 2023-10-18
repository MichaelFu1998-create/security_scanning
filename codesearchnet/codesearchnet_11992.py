def color_features(in_objectinfo,
                   deredden=True,
                   custom_bandpasses=None,
                   dust_timeout=10.0):
    '''Stellar colors and dereddened stellar colors using 2MASS DUST API:

    http://irsa.ipac.caltech.edu/applications/DUST/docs/dustProgramInterface.html

    Parameters
    ----------

    in_objectinfo : dict
        This is a dict that contains the object's magnitudes and positions. This
        requires at least 'ra', and 'decl' as keys which correspond to the right
        ascension and declination of the object, and one or more of the
        following keys for object magnitudes::

            'umag'  -> U mag             -> colors: U-B, U-V, U-g
            'bmag'  -> B mag             -> colors: U-B, B-V
            'vmag'  -> V mag             -> colors: U-V, B-V, V-R, V-I, V-K
            'rmag'  -> R mag             -> colors: V-R, R-I
            'imag'  -> I mag             -> colors: g-I, V-I, R-I, B-I
            'jmag'  -> 2MASS J mag       -> colors: J-H, J-K, g-J, i-J
            'hmag'  -> 2MASS H mag       -> colors: J-H, H-K
            'kmag'  -> 2MASS Ks mag      -> colors: g-Ks, H-Ks, J-Ks, V-Ks
            'sdssu' -> SDSS u mag        -> colors: u-g, u-V
            'sdssg' -> SDSS g mag        -> colors: g-r, g-i, g-K, u-g, U-g, g-J
            'sdssr' -> SDSS r mag        -> colors: r-i, g-r
            'sdssi' -> SDSS i mag        -> colors: r-i, i-z, g-i, i-J, i-W1
            'sdssz' -> SDSS z mag        -> colors: i-z, z-W2, g-z
            'ujmag' -> UKIRT J mag       -> colors: J-H, H-K, J-K, g-J, i-J
            'uhmag' -> UKIRT H mag       -> colors: J-H, H-K
            'ukmag' -> UKIRT K mag       -> colors: g-K, H-K, J-K, V-K
            'irac1' -> Spitzer IRAC1 mag -> colors: i-I1, I1-I2
            'irac2' -> Spitzer IRAC2 mag -> colors: I1-I2, I2-I3
            'irac3' -> Spitzer IRAC3 mag -> colors: I2-I3
            'irac4' -> Spitzer IRAC4 mag -> colors: I3-I4
            'wise1' -> WISE W1 mag       -> colors: i-W1, W1-W2
            'wise2' -> WISE W2 mag       -> colors: W1-W2, W2-W3
            'wise3' -> WISE W3 mag       -> colors: W2-W3
            'wise4' -> WISE W4 mag       -> colors: W3-W4

        These are basically taken from the available reddening bandpasses from
        the 2MASS DUST service. If B, V, u, g, r, i, z aren't provided but 2MASS
        J, H, Ks are all provided, the former will be calculated using the 2MASS
        JHKs -> BVugriz conversion functions in :py:mod:`astrobase.magnitudes`.

    deredden : bool
        If True, will make sure all colors use dereddened mags where possible.

    custom_bandpasses : dict
        This is a dict used to define any custom bandpasses in the
        `in_objectinfo` dict you want to make this function aware of and
        generate colors for. Use the format below for this dict::

            {
            '<bandpass_key_1>':{'dustkey':'<twomass_dust_key_1>',
                                'label':'<band_label_1>'
                                'colors':[['<bandkey1>-<bandkey2>',
                                           '<BAND1> - <BAND2>'],
                                          ['<bandkey3>-<bandkey4>',
                                           '<BAND3> - <BAND4>']]},
            .
            ...
            .
            '<bandpass_key_N>':{'dustkey':'<twomass_dust_key_N>',
                                'label':'<band_label_N>'
                                'colors':[['<bandkey1>-<bandkey2>',
                                           '<BAND1> - <BAND2>'],
                                          ['<bandkey3>-<bandkey4>',
                                           '<BAND3> - <BAND4>']]},
            }

        Where:

        `bandpass_key` is a key to use to refer to this bandpass in the
        `objectinfo` dict, e.g. 'sdssg' for SDSS g band

        `twomass_dust_key` is the key to use in the 2MASS DUST result table for
        reddening per band-pass. For example, given the following DUST result
        table (using http://irsa.ipac.caltech.edu/applications/DUST/)::

            |Filter_name|LamEff |A_over_E_B_V_SandF|A_SandF|A_over_E_B_V_SFD|A_SFD|
            |char       |float  |float             |float  |float           |float|
            |           |microns|                  |mags   |                |mags |
             CTIO U       0.3734              4.107   0.209            4.968 0.253
             CTIO B       0.4309              3.641   0.186            4.325 0.221
             CTIO V       0.5517              2.682   0.137            3.240 0.165
            .
            .
            ...

        The `twomass_dust_key` for 'vmag' would be 'CTIO V'. If you want to
        skip DUST lookup and want to pass in a specific reddening magnitude
        for your bandpass, use a float for the value of
        `twomass_dust_key`. If you want to skip DUST lookup entirely for
        this bandpass, use None for the value of `twomass_dust_key`.

        `band_label` is the label to use for this bandpass, e.g. 'W1' for
        WISE-1 band, 'u' for SDSS u, etc.

        The 'colors' list contains color definitions for all colors you want
        to generate using this bandpass. this list contains elements of the
        form::

            ['<bandkey1>-<bandkey2>','<BAND1> - <BAND2>']

        where the the first item is the bandpass keys making up this color,
        and the second item is the label for this color to be used by the
        frontends. An example::

            ['sdssu-sdssg','u - g']

    dust_timeout : float
        The timeout to use when contacting the 2MASS DUST web service.

    Returns
    -------

    dict
        An `objectinfo` dict with all of the generated colors, dereddened
        magnitude,s dereddened colors, as specified in the input args is
        returned.

    '''

    objectinfo = in_objectinfo.copy()

    # this is the initial output dict
    outdict = {
        'available_bands':[],
        'available_band_labels':[],
        'available_dereddened_bands':[],
        'available_dereddened_band_labels':[],
        'available_colors':[],
        'available_color_labels':[],
        'dereddened':False
    }

    #
    # get the BVugriz mags from the JHK mags if necessary
    #
    # FIXME: should these be direct dered mag_0 = f(J_0, H_0, K_0) instead?
    # Bilir+ 2008 uses dereddened colors for their transforms, should check if
    # we need to do so here

    if ('jmag' in objectinfo and
        objectinfo['jmag'] is not None and
        np.isfinite(objectinfo['jmag']) and
        'hmag' in objectinfo and
        objectinfo['hmag'] is not None and
        np.isfinite(objectinfo['hmag']) and
        'kmag' in objectinfo and
        objectinfo['kmag'] is not None and
        np.isfinite(objectinfo['kmag'])):

        if ('bmag' not in objectinfo or
            ('bmag' in objectinfo and objectinfo['bmag'] is None) or
            ('bmag' in objectinfo and not np.isfinite(objectinfo['bmag']))):
            objectinfo['bmag'] = magnitudes.jhk_to_bmag(objectinfo['jmag'],
                                                        objectinfo['hmag'],
                                                        objectinfo['kmag'])
            outdict['bmagfromjhk'] = True
        else:
            outdict['bmagfromjhk'] = False

        if ('vmag' not in objectinfo or
            ('vmag' in objectinfo and objectinfo['vmag'] is None) or
            ('vmag' in objectinfo and not np.isfinite(objectinfo['vmag']))):
            objectinfo['vmag'] = magnitudes.jhk_to_vmag(objectinfo['jmag'],
                                                        objectinfo['hmag'],
                                                        objectinfo['kmag'])
            outdict['vmagfromjhk'] = True
        else:
            outdict['vmagfromjhk'] = False


        if ('sdssu' not in objectinfo or
            ('sdssu' in objectinfo and objectinfo['sdssu'] is None) or
            ('sdssu' in objectinfo and not np.isfinite(objectinfo['sdssu']))):
            objectinfo['sdssu'] = magnitudes.jhk_to_sdssu(objectinfo['jmag'],
                                                          objectinfo['hmag'],
                                                          objectinfo['kmag'])
            outdict['sdssufromjhk'] = True
        else:
            outdict['sdssufromjhk'] = False

        if ('sdssg' not in objectinfo or
            ('sdssg' in objectinfo and objectinfo['sdssg'] is None) or
            ('sdssg' in objectinfo and not np.isfinite(objectinfo['sdssg']))):
            objectinfo['sdssg'] = magnitudes.jhk_to_sdssg(objectinfo['jmag'],
                                                          objectinfo['hmag'],
                                                          objectinfo['kmag'])
            outdict['sdssgfromjhk'] = True
        else:
            outdict['sdssgfromjhk'] = False

        if ('sdssr' not in objectinfo or
            ('sdssr' in objectinfo and objectinfo['sdssr'] is None) or
            ('sdssr' in objectinfo and not np.isfinite(objectinfo['sdssr']))):
            objectinfo['sdssr'] = magnitudes.jhk_to_sdssr(objectinfo['jmag'],
                                                          objectinfo['hmag'],
                                                          objectinfo['kmag'])
            outdict['sdssrfromjhk'] = True
        else:
            outdict['sdssrfromjhk'] = False

        if ('sdssi' not in objectinfo or
            ('sdssi' in objectinfo and objectinfo['sdssi'] is None) or
            ('sdssi' in objectinfo and not np.isfinite(objectinfo['sdssi']))):
            objectinfo['sdssi'] = magnitudes.jhk_to_sdssi(objectinfo['jmag'],
                                                          objectinfo['hmag'],
                                                          objectinfo['kmag'])
            outdict['sdssifromjhk'] = True
        else:
            outdict['sdssifromjhk'] = False

        if ('sdssz' not in objectinfo or
            ('sdssz' in objectinfo and objectinfo['sdssz'] is None) or
            ('sdssz' in objectinfo and not np.isfinite(objectinfo['sdssz']))):
            objectinfo['sdssz'] = magnitudes.jhk_to_sdssz(objectinfo['jmag'],
                                                          objectinfo['hmag'],
                                                          objectinfo['kmag'])
            outdict['sdsszfromjhk'] = True
        else:
            outdict['sdsszfromjhk'] = False


    # now handle dereddening if possible
    if deredden:

        try:

            # first, get the extinction table for this object
            extinction = dust.extinction_query(objectinfo['ra'],
                                               objectinfo['decl'],
                                               verbose=False,
                                               timeout=dust_timeout)

        except Exception as e:

            LOGERROR("deredden = True but 'ra', 'decl' keys not present "
                     "or invalid in objectinfo dict, ignoring reddening...")
            extinction = None
            outdict['dereddened'] = False

    else:

        extinction = None
        outdict['dereddened'] = False

    # handle timeout from DUST service
    if not extinction:
        outdict['dereddened'] = False

    # go through the objectdict and pick out the mags we have available from the
    # BANDPASSES_COLORS dict

    # update our bandpasses_colors dict with any custom ones the user defined
    our_bandpasses_colors = BANDPASSES_COLORS.copy()
    our_bandpass_list = BANDPASS_LIST[::]

    if custom_bandpasses is not None and isinstance(custom_bandpasses, dict):

        our_bandpasses_colors.update(custom_bandpasses)

        # also update the list
        for key in custom_bandpasses:
            if key not in our_bandpass_list:
                our_bandpass_list.append(key)

    for mk in our_bandpass_list:

        if (mk in objectinfo and
            objectinfo[mk] is not None and
            np.isfinite(objectinfo[mk])):

            thisbandlabel = our_bandpasses_colors[mk]['label']
            thisdustkey = our_bandpasses_colors[mk]['dustkey']

            # add this to the outdict
            outdict[mk] = objectinfo[mk]

            outdict['available_bands'].append(mk)
            outdict['available_band_labels'].append(thisbandlabel)

            #
            # deredden if possible
            #
            # calculating dereddened mags:
            # A_x = m - m0_x where m is measured mag, m0 is intrinsic mag
            # m0_x = m - A_x
            #
            # so for two bands x, y:
            # intrinsic color (m_x - m_y)_0 = (m_x - m_y) - (A_x - A_y)
            if (deredden and extinction):

                outdict['dereddened'] = True

                # check if the dustkey is None, float, or str to figure out how
                # to retrieve the reddening
                if (thisdustkey is not None and
                    isinstance(thisdustkey, str) and
                    thisdustkey in extinction['Amag'] and
                    np.isfinite(extinction['Amag'][thisdustkey]['sf11'])):

                    outdict['extinction_%s' % mk] = (
                        extinction['Amag'][thisdustkey]['sf11']
                    )

                elif (thisdustkey is not None and
                      isinstance(thisdustkey, float)):

                    outdict['extinction_%s' % mk] = thisdustkey

                else:

                    outdict['extinction_%s' % mk] = 0.0

                # apply the extinction
                outdict['dered_%s' % mk] = (
                    outdict[mk] - outdict['extinction_%s' % mk]
                )
                outdict['available_dereddened_bands'].append('dered_%s' % mk)
                outdict['available_dereddened_band_labels'].append(
                    thisbandlabel
                )

                # get all the colors to generate for this bandpass
                for colorspec in BANDPASSES_COLORS[mk]['colors']:

                    # only add this if the color's not there already
                    if colorspec[0] not in outdict:

                        colorkey, colorlabel = colorspec

                        # look for the bands to make this color

                        # if it's not found now, this should work when we come
                        # around for the next bandpass for this color

                        band1, band2 = colorkey.split('-')

                        if ('dered_%s' % band1 in outdict and
                            'dered_%s' % band2 in outdict and
                            np.isfinite(outdict['dered_%s' % band1]) and
                            np.isfinite(outdict['dered_%s' % band2])):

                            outdict[colorkey] = (
                                outdict['dered_%s' % band1] -
                                outdict['dered_%s' % band2]
                            )
                            outdict['available_colors'].append(colorkey)
                            outdict['available_color_labels'].append(colorlabel)


            # handle no dereddening
            else:

                outdict['dereddened'] = False
                outdict['extinction_%s' % mk] = 0.0
                outdict['dered_%s' % mk] = np.nan

                # get all the colors to generate for this bandpass
                for colorspec in our_bandpasses_colors[mk]['colors']:

                    # only add this if the color's not there already
                    if colorspec[0] not in outdict:

                        colorkey, colorlabel = colorspec

                        # look for the bands to make this color

                        # if it's not found now, this should work when we come
                        # around for the next bandpass for this color

                        band1, band2 = colorkey.split('-')

                        if (band1 in outdict and
                            band2 in outdict and
                            outdict[band1] is not None and
                            outdict[band2] is not None and
                            np.isfinite(outdict[band1]) and
                            np.isfinite(outdict[band2])):

                            outdict[colorkey] = (
                                outdict[band1] -
                                outdict[band2]
                            )
                            outdict['available_colors'].append(colorkey)
                            outdict['available_color_labels'].append(colorlabel)


        # if this bandpass was not found in the objectinfo dict, ignore it
        else:

            outdict[mk] = np.nan


    return outdict