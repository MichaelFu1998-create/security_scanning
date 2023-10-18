def jhk_to_bmag(jmag, hmag, kmag):
    '''Converts given J, H, Ks mags to a B magnitude value.

    Parameters
    ----------

    jmag,hmag,kmag : float
        2MASS J, H, Ks mags of the object.

    Returns
    -------

    float
        The converted B band magnitude.

    '''

    return convert_constants(jmag,hmag,kmag,
                             BJHK,
                             BJH, BJK, BHK,
                             BJ, BH, BK)