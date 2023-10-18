def generalized_lsp_value_notau(times, mags, errs, omega):
    '''
    This is the simplified version not using tau.

    The relations used are::

        W = sum (1.0/(errs*errs) )
        w_i = (1/W)*(1/(errs*errs))

        Y = sum( w_i*y_i )
        C = sum( w_i*cos(wt_i) )
        S = sum( w_i*sin(wt_i) )

        YY = sum( w_i*y_i*y_i ) - Y*Y
        YC = sum( w_i*y_i*cos(wt_i) ) - Y*C
        YS = sum( w_i*y_i*sin(wt_i) ) - Y*S

        CpC = sum( w_i*cos(w_t_i)*cos(w_t_i) )
        CC = CpC - C*C
        SS = (1 - CpC) - S*S
        CS = sum( w_i*cos(w_t_i)*sin(w_t_i) ) - C*S

        D(omega) = CC*SS - CS*CS
        P(omega) = (SS*YC*YC + CC*YS*YS - 2.0*CS*YC*YS)/(YY*D)

    Parameters
    ----------

    times,mags,errs : np.array
        The time-series to calculate the periodogram value for.

    omega : float
        The frequency to calculate the periodogram value at.

    Returns
    -------

    periodogramvalue : float
        The normalized periodogram at the specified test frequency `omega`.

    '''

    one_over_errs2 = 1.0/(errs*errs)

    W = npsum(one_over_errs2)
    wi = one_over_errs2/W

    sin_omegat = npsin(omega*times)
    cos_omegat = npcos(omega*times)

    sin2_omegat = sin_omegat*sin_omegat
    cos2_omegat = cos_omegat*cos_omegat
    sincos_omegat = sin_omegat*cos_omegat

    # calculate some more sums and terms
    Y = npsum( wi*mags )
    C = npsum( wi*cos_omegat )
    S = npsum( wi*sin_omegat )

    YpY = npsum( wi*mags*mags)

    YpC = npsum( wi*mags*cos_omegat )
    YpS = npsum( wi*mags*sin_omegat )

    CpC = npsum( wi*cos2_omegat )
    # SpS = npsum( wi*sin2_omegat )

    CpS = npsum( wi*sincos_omegat )

    # the final terms
    YY = YpY - Y*Y
    YC = YpC - Y*C
    YS = YpS - Y*S
    CC = CpC - C*C
    SS = 1 - CpC - S*S  # use SpS = 1 - CpC
    CS = CpS - C*S

    # P(omega) = (SS*YC*YC + CC*YS*YS - 2.0*CS*YC*YS)/(YY*D)
    # D(omega) = CC*SS - CS*CS
    Domega = CC*SS - CS*CS
    lspval = (SS*YC*YC + CC*YS*YS - 2.0*CS*YC*YS)/(YY*Domega)

    return lspval