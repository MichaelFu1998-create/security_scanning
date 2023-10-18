def position_CD(Ka,out_type = 'fb_exact'):
    """
    CD sled position control case study of Chapter 18.

    The function returns the closed-loop and open-loop
    system function for a CD/DVD sled position control
    system. The loop amplifier gain is the only variable
    that may be changed. The returned system function can
    however be changed.

    Parameters
    ----------
    Ka : loop amplifier gain, start with 50.
    out_type : 'open_loop' for open loop system function
    out_type : 'fb_approx' for closed-loop approximation
    out_type : 'fb_exact' for closed-loop exact

    Returns
    -------
    b : numerator coefficient ndarray
    a : denominator coefficient ndarray 

    Notes
    -----
    With the exception of the loop amplifier gain, all
    other parameters are hard-coded from Case Study example.

    Examples
    --------
    >>> b,a = position_CD(Ka,'fb_approx')
    >>> b,a = position_CD(Ka,'fb_exact')
    """
    rs = 10/(2*np.pi)
    # Load b and a ndarrays with the coefficients
    if out_type.lower() == 'open_loop':
        b = np.array([Ka*4000*rs])
        a = np.array([1,1275,31250,0])
    elif out_type.lower() == 'fb_approx':
        b = np.array([3.2*Ka*rs])
        a = np.array([1, 25, 3.2*Ka*rs])
    elif out_type.lower() == 'fb_exact':
        b = np.array([4000*Ka*rs])
        a = np.array([1, 1250+25, 25*1250, 4000*Ka*rs])
    else:
        raise ValueError('out_type must be: open_loop, fb_approx, or fc_exact')
    return b, a