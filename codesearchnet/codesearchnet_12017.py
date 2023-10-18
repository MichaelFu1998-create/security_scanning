def townsend_lombscargle_value(times, mags, omega):
    '''
    This calculates the periodogram value for each omega (= 2*pi*f). Mags must
    be normalized to zero with variance scaled to unity.

    '''
    cos_omegat = npcos(omega*times)
    sin_omegat = npsin(omega*times)

    xc = npsum(mags*cos_omegat)
    xs = npsum(mags*sin_omegat)

    cc = npsum(cos_omegat*cos_omegat)
    ss = npsum(sin_omegat*sin_omegat)

    cs = npsum(cos_omegat*sin_omegat)

    tau = nparctan(2*cs/(cc - ss))/(2*omega)

    ctau = npcos(omega*tau)
    stau = npsin(omega*tau)

    leftsumtop = (ctau*xc + stau*xs)*(ctau*xc + stau*xs)
    leftsumbot = ctau*ctau*cc + 2.0*ctau*stau*cs + stau*stau*ss
    leftsum = leftsumtop/leftsumbot

    rightsumtop = (ctau*xs - stau*xc)*(ctau*xs - stau*xc)
    rightsumbot = ctau*ctau*ss - 2.0*ctau*stau*cs + stau*stau*cc
    rightsum = rightsumtop/rightsumbot

    pval = 0.5*(leftsum + rightsum)

    return pval