def mdwarf_subtype_from_sdsscolor(ri_color, iz_color):
    '''This calculates the M-dwarf subtype given SDSS `r-i` and `i-z` colors.

    Parameters
    ----------

    ri_color : float
        The SDSS `r-i` color of the object.

    iz_color : float
        The SDSS `i-z` color of the object.

    Returns
    -------

    (subtype, index1, index2) : tuple
        `subtype`: if the star appears to be an M dwarf, will return an int
        between 0 and 9 indicating its subtype, e.g. will return 4 for an M4
        dwarf. If the object isn't an M dwarf, will return None

        `index1`, `index2`: the M-dwarf color locus value and spread of this
        object calculated from the `r-i` and `i-z` colors.

    '''

    # calculate the spectral type index and the spectral type spread of the
    # object. sti is calculated by fitting a line to the locus in r-i and i-z
    # space for M dwarfs in West+ 2007
    if np.isfinite(ri_color) and np.isfinite(iz_color):
        obj_sti = 0.875274*ri_color + 0.483628*(iz_color + 0.00438)
        obj_sts = -0.483628*ri_color + 0.875274*(iz_color + 0.00438)
    else:
        obj_sti = np.nan
        obj_sts = np.nan

    # possible M star if sti is >= 0.666 but <= 3.4559
    if (np.isfinite(obj_sti) and np.isfinite(obj_sts) and
        (obj_sti > 0.666) and (obj_sti < 3.4559)):

        # decide which M subclass object this is
        if ((obj_sti > 0.6660) and (obj_sti < 0.8592)):
            m_class = 'M0'

        if ((obj_sti > 0.8592) and (obj_sti < 1.0822)):
            m_class = 'M1'

        if ((obj_sti > 1.0822) and (obj_sti < 1.2998)):
            m_class = 'M2'

        if ((obj_sti > 1.2998) and (obj_sti < 1.6378)):
            m_class = 'M3'

        if ((obj_sti > 1.6378) and (obj_sti < 2.0363)):
            m_class = 'M4'

        if ((obj_sti > 2.0363) and (obj_sti < 2.2411)):
            m_class = 'M5'

        if ((obj_sti > 2.2411) and (obj_sti < 2.4126)):
            m_class = 'M6'

        if ((obj_sti > 2.4126) and (obj_sti < 2.9213)):
            m_class = 'M7'

        if ((obj_sti > 2.9213) and (obj_sti < 3.2418)):
            m_class = 'M8'

        if ((obj_sti > 3.2418) and (obj_sti < 3.4559)):
            m_class = 'M9'

    else:
        m_class = None

    return m_class, obj_sti, obj_sts