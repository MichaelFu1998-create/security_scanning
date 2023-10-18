def jhk_to_vmag(jmag,hmag,kmag):
    '''Converts given J, H, Ks mags to a V magnitude value.

    Parameters
    ----------

    jmag,hmag,kmag : float
        2MASS J, H, Ks mags of the object.

    Returns
    -------

    float
        The converted V band magnitude.

    '''

    return convert_constants(jmag,hmag,kmag,
                             VJHK,
                             VJH, VJK, VHK,
                             VJ, VH, VK)