def jhk_to_rmag(jmag,hmag,kmag):
    '''Converts given J, H, Ks mags to an R magnitude value.

    Parameters
    ----------

    jmag,hmag,kmag : float
        2MASS J, H, Ks mags of the object.

    Returns
    -------

    float
        The converted R band magnitude.

    '''

    return convert_constants(jmag,hmag,kmag,
                             RJHK,
                             RJH, RJK, RHK,
                             RJ, RH, RK)