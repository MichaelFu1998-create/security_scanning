def color_classification(colorfeatures, pmfeatures):
    '''This calculates rough star type classifications based on star colors
    in the ugrizJHK bands.

    Uses the output from `color_features` and `coord_features`. By default,
    `color_features` will use dereddened colors, as are expected by most
    relations here.

    Based on the color cuts from:

    - SDSS SEGUE (Yanny+ 2009)
    - SDSS QSO catalog (Schneider+ 2007)
    - SDSS RR Lyrae catalog (Sesar+ 2011)
    - SDSS M-dwarf catalog (West+ 2008)
    - Helmi+ 2003
    - Bochanski+ 2014

    Parameters
    ----------

    colorfeatures : dict
        This is the dict produced by the `color_features` function.

    pmfeatures : dict
        This is the dict produced by the `coord_features` function.

    Returns
    -------

    dict
        A dict containing all of the possible classes this object can belong to
        as a list in the `color_classes` key, and values of the various color
        indices used to arrive to that conclusion as the other keys.

    '''

    possible_classes = []

    if not colorfeatures:
        return possible_classes

    if not pmfeatures:
        return possible_classes

    # dered mags
    if ( ('dered_sdssu' in colorfeatures) and
         (colorfeatures['dered_sdssu'] is not None) and
         (np.isfinite(colorfeatures['dered_sdssu'])) ):
        u = colorfeatures['dered_sdssu']
    else:
        u = np.nan

    if ( ('dered_sdssg' in colorfeatures) and
         (colorfeatures['dered_sdssg'] is not None) and
         (np.isfinite(colorfeatures['dered_sdssg'])) ):
        g = colorfeatures['dered_sdssg']
    else:
        g = np.nan

    if ( ('dered_sdssr' in colorfeatures) and
         (colorfeatures['dered_sdssr'] is not None) and
         (np.isfinite(colorfeatures['dered_sdssr'])) ):
        r = colorfeatures['dered_sdssr']
    else:
        r = np.nan

    if ( ('dered_sdssi' in colorfeatures) and
         (colorfeatures['dered_sdssi'] is not None) and
         (np.isfinite(colorfeatures['dered_sdssi'])) ):
        i = colorfeatures['dered_sdssi']
    else:
        i = np.nan

    if ( ('dered_sdssz' in colorfeatures) and
         (colorfeatures['dered_sdssz'] is not None) and
         (np.isfinite(colorfeatures['dered_sdssz'])) ):
        z = colorfeatures['dered_sdssz']
    else:
        z = np.nan

    if ( ('dered_jmag' in colorfeatures) and
         (colorfeatures['dered_jmag'] is not None) and
         (np.isfinite(colorfeatures['dered_jmag'])) ):
        j = colorfeatures['dered_jmag']
    else:
        j = np.nan

    if ( ('dered_hmag' in colorfeatures) and
         (colorfeatures['dered_hmag'] is not None) and
         (np.isfinite(colorfeatures['dered_hmag'])) ):
        h = colorfeatures['dered_hmag']
    else:
        h = np.nan

    if ( ('dered_kmag' in colorfeatures) and
         (colorfeatures['dered_kmag'] is not None) and
         (np.isfinite(colorfeatures['dered_kmag'])) ):
        k = colorfeatures['dered_kmag']
    else:
        k = np.nan


    # measured mags
    if 'sdssu' in colorfeatures and colorfeatures['sdssu'] is not None:
        um = colorfeatures['sdssu']
    else:
        um = np.nan
    if 'sdssg' in colorfeatures and colorfeatures['sdssg'] is not None:
        gm = colorfeatures['sdssg']
    else:
        gm = np.nan
    if 'sdssr' in colorfeatures and colorfeatures['sdssr'] is not None:
        rm = colorfeatures['sdssr']
    else:
        rm = np.nan
    if 'sdssi' in colorfeatures and colorfeatures['sdssi'] is not None:
        im = colorfeatures['sdssi']
    else:
        im = np.nan
    if 'sdssz' in colorfeatures and colorfeatures['sdssz'] is not None:
        zm = colorfeatures['sdssz']
    else:
        zm = np.nan
    if 'jmag' in colorfeatures and colorfeatures['jmag'] is not None:
        jm = colorfeatures['jmag']
    else:
        jm = np.nan
    if 'hmag' in colorfeatures and colorfeatures['hmag'] is not None:
        hm = colorfeatures['hmag']
    else:
        hm = np.nan
    if 'kmag' in colorfeatures and colorfeatures['kmag'] is not None:
        km = colorfeatures['kmag']
    else:
        km = np.nan


    # reduced proper motion
    rpmj = pmfeatures['rpmj'] if np.isfinite(pmfeatures['rpmj']) else None

    # now generate the various color indices
    # color-gravity index
    if (np.isfinite(u) and np.isfinite(g) and
        np.isfinite(r) and np.isfinite(i) and
        np.isfinite(z)):
        v_color = 0.283*(u-g)-0.354*(g-r)+0.455*(r-i)+0.766*(i-z)
    else:
        v_color = np.nan

    # metallicity index p1
    if (np.isfinite(u) and np.isfinite(g) and np.isfinite(r)):
        p1_color = 0.91*(u-g)+0.415*(g-r)-1.28
    else:
        p1_color = np.nan

    # metallicity index l
    if (np.isfinite(u) and np.isfinite(g) and
        np.isfinite(r) and np.isfinite(i)):
        l_color = -0.436*u + 1.129*g - 0.119*r - 0.574*i + 0.1984
    else:
        l_color = np.nan

    # metallicity index s
    if (np.isfinite(u) and np.isfinite(g) and np.isfinite(r)):
        s_color = -0.249*u + 0.794*g - 0.555*r + 0.124
    else:
        s_color = np.nan

    # RR Lyrae ug and gr indexes
    if (np.isfinite(u) and np.isfinite(g) and np.isfinite(r)):
        d_ug = (u-g) + 0.67*(g-r) - 1.07
        d_gr = 0.45*(u-g) - (g-r) - 0.12
    else:
        d_ug, d_gr = np.nan, np.nan


    # check the M subtype
    m_subtype, m_sti, m_sts = mdwarf_subtype_from_sdsscolor(r-i, i-z)

    # now check if this is a likely M dwarf
    if m_subtype and rpmj and rpmj > 1.0:
        possible_classes.append('d' + m_subtype)

    # white dwarf
    if ( np.isfinite(u) and np.isfinite(g) and np.isfinite(r) and
         ((g-r) < -0.2) and ((g-r) > -1.0) and
         ((u-g) < 0.7) and ((u-g) > -1) and
         ((u-g+2*(g-r)) < -0.1) ):
        possible_classes.append('WD/sdO/sdB')

    # A/BHB/BStrg
    if ( np.isfinite(u) and np.isfinite(g) and np.isfinite(r) and
         ((u-g) < 1.5) and ((u-g) > 0.8) and
         ((g-r) < 0.2) and ((g-r) > -0.5) ):
        possible_classes.append('A/BHB/blustrg')

    # F turnoff/sub-dwarf
    if ( (np.isfinite(p1_color) and np.isfinite(p1_color) and
          np.isfinite(u) and np.isfinite(g) and np.isfinite(r) ) and
         (p1_color < -0.25) and (p1_color > -0.7) and
         ((u-g) < 1.4) and ((u-g) > 0.4) and
         ((g-r) < 0.7) and ((g-r) > 0.2) ):
        possible_classes.append('Fturnoff/sdF')

    # low metallicity
    if ( (np.isfinite(u) and np.isfinite(g) and np.isfinite(r) and
          np.isfinite(l_color)) and
         ((g-r) < 0.75) and ((g-r) > -0.5) and
         ((u-g) < 3.0) and ((u-g) > 0.6) and
         (l_color > 0.135) ):
        possible_classes.append('lowmetal')

    # low metallicity giants from Helmi+ 2003
    if ( (np.isfinite(p1_color) and np.isfinite(s_color)) and
         (-0.1 < p1_color < 0.6) and (s_color > 0.05) ):
        possible_classes.append('lowmetalgiant')

    # F/G star
    if ( (np.isfinite(g) and np.isfinite(g) and np.isfinite(r)) and
         ((g-r) < 0.48) and ((g-r) > 0.2) ):
        possible_classes.append('F/G')

    # G dwarf
    if ( (np.isfinite(g) and np.isfinite(r)) and
         ((g-r) < 0.55) and ((g-r) > 0.48) ):
        possible_classes.append('dG')

    # K giant
    if ( (np.isfinite(u) and np.isfinite(g) and
          np.isfinite(r) and np.isfinite(i) and
          np.isfinite(l_color)) and
         ((g-r) > 0.35) and ((g-r) < 0.7) and
         (l_color > 0.07) and ((u-g) > 0.7) and ((u-g) < 4.0) and
         ((r-i) > 0.15) and ((r-i) < 0.6) ):
        possible_classes.append('gK')

    # AGB
    if ( (np.isfinite(u) and np.isfinite(g) and
          np.isfinite(r) and np.isfinite(s_color)) and
         ((u-g) < 3.5) and ((u-g) > 2.5) and
         ((g-r) < 1.3) and ((g-r) > 0.9) and
         (s_color < -0.06) ):
        possible_classes.append('AGB')

    # K dwarf
    if ( (np.isfinite(g) and np.isfinite(r)) and
         ((g-r) < 0.75) and ((g-r) > 0.55) ):
        possible_classes.append('dK')

    # M subdwarf
    if ( (np.isfinite(g) and np.isfinite(r) and np.isfinite(i)) and
         ((g-r) > 1.6) and ((r-i) < 1.3) and ((r-i) > 0.95) ):
        possible_classes.append('sdM')

    # M giant colors from Bochanski+ 2014
    if ( (np.isfinite(j) and np.isfinite(h) and np.isfinite(k) and
          np.isfinite(g) and np.isfinite(i)) and
         ((j-k) > 1.02) and
         ((j-h) < (0.561*(j-k) + 0.46)) and
         ((j-h) > (0.561*(j-k) + 0.14)) and
         ((g-i) > (0.932*(i-k) - 0.872)) ):
        possible_classes.append('gM')

    # MS+WD pair
    if ( (np.isfinite(um) and np.isfinite(gm) and
          np.isfinite(rm) and np.isfinite(im)) and
         ((um-gm) < 2.25) and ((gm-rm) > -0.2) and
         ((gm-rm) < 1.2) and ((rm-im) > 0.5) and
         ((rm-im) < 2.0) and
         ((gm-rm) > (-19.78*(rm-im)+11.13)) and
         ((gm-rm) < (0.95*(rm-im)+0.5)) ):
        possible_classes.append('MSWD')

    # brown dwarf
    if ( (np.isfinite(um) and np.isfinite(gm) and np.isfinite(rm) and
          np.isfinite(im) and np.isfinite(zm)) and
         (zm < 19.5) and (um > 21.0) and (gm > 22.0) and
         (rm > 21.0) and ((im - zm) > 1.7) ):
        possible_classes.append('BD')

    # RR Lyrae candidate
    if ( (np.isfinite(u) and np.isfinite(g) and np.isfinite(r) and
          np.isfinite(i) and np.isfinite(z) and np.isfinite(d_ug) and
          np.isfinite(d_gr)) and
         ((u-g) > 0.98) and ((u-g) < 1.3) and
         (d_ug > -0.05) and (d_ug < 0.35) and
         (d_gr > 0.06) and (d_gr < 0.55) and
         ((r-i) > -0.15) and ((r-i) < 0.22) and
         ((i-z) > -0.21) and ((i-z) < 0.25) ):
        possible_classes.append('RRL')

    # QSO color
    if ( (np.isfinite(u) and np.isfinite(g) and np.isfinite(r)) and
         ( (((u-g) > -0.1) and ((u-g) < 0.7) and
            ((g-r) > -0.3) and ((g-r) < 0.5)) or
           ((u-g) > (1.6*(g-r) + 1.34)) ) ):
        possible_classes.append('QSO')

    return {'color_classes':possible_classes,
            'v_color':v_color,
            'p1_color':p1_color,
            's_color':s_color,
            'l_color':l_color,
            'd_ug':d_ug,
            'd_gr':d_gr,
            'm_sti':m_sti,
            'm_sts':m_sts}