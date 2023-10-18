def should_particle_exist(absent_err, present_err, absent_d, present_d,
                          im_change_frac=0.2, min_derr=0.1):
    """
    Checks whether or not adding a particle should be present.

    Parameters
    ----------
    absent_err : Float
        The state error without the particle.
    present_err : Float
        The state error with the particle.
    absent_d : numpy.ndarray
        The state residuals without the particle.
    present_d : numpy.ndarray
        The state residuals with the particle.
    im_change_frac : Float, optional
        How good the change in error needs to be relative to the change in
        the residuals. Default is 0.2; i.e. return False if the error does
        not decrease by 0.2 x the change in the residuals.
    min_derr : Float, optional
        The minimal improvement in error. Default is 0.1

    Returns
    -------
    Bool
        True if the errors is better with the particle present.
    """
    delta_im = np.ravel(present_d - absent_d)
    im_change = np.dot(delta_im, delta_im)
    err_cutoff = max([im_change_frac * im_change, min_derr])
    return (absent_err - present_err) >= err_cutoff