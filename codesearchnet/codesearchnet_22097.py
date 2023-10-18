def BDES2K(bdes, quad_length, energy):
    """
    Converts a quadrupole :math:`B_des` into a geometric focusing strength :math:`K`.

    Parameters
    ----------

    bdes : float
        The magnet value of :math:`B_des`.
    quad_length : float
        The length of the quadrupole in meters.
    energy : float
        The design energy of the beam in GeV.

    Returns
    -------
    K : float
        The geometric focusing strength :math:`K`.
    """
    # Make sure everything is float
    bdes        = _np.float_(bdes)
    quad_length = _np.float_(quad_length)
    energy      = _np.float_(energy)

    Brho = energy/_np.float_(0.029979)
    K = bdes/(Brho*quad_length)
    logger.log(level=loggerlevel, msg='Converted BDES: {bdes}, quad length: {quad_length}, energy: {energy} to K: {K}'.format(
        bdes        = bdes        ,
        quad_length = quad_length ,
        energy      = energy      ,
        K           = K
        )
        )

    return K