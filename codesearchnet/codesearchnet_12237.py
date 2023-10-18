def generalized_lsp_value(times, mags, errs, omega):
    '''Generalized LSP value for a single omega.

    The relations used are::

        P(w) = (1/YY) * (YC*YC/CC + YS*YS/SS)

        where: YC, YS, CC, and SS are all calculated at T

        and where: tan 2omegaT = 2*CS/(CC - SS)

        and where:

        Y = sum( w_i*y_i )
        C = sum( w_i*cos(wT_i) )
        S = sum( w_i*sin(wT_i) )

        YY = sum( w_i*y_i*y_i ) - Y*Y
        YC = sum( w_i*y_i*cos(wT_i) ) - Y*C
        YS = sum( w_i*y_i*sin(wT_i) ) - Y*S

        CpC = sum( w_i*cos(w_T_i)*cos(w_T_i) )
        CC = CpC - C*C
        SS = (1 - CpC) - S*S
        CS = sum( w_i*cos(w_T_i)*sin(w_T_i) ) - C*S

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

    CpS = npsum( wi*sincos_omegat )
    CpC = npsum( wi*cos2_omegat )
    CS = CpS - C*S
    CC = CpC - C*C
    SS = 1 - CpC - S*S  # use SpS = 1 - CpC

    # calculate tau
    tan_omega_tau_top = 2.0*CS
    tan_omega_tau_bottom = CC - SS
    tan_omega_tau = tan_omega_tau_top/tan_omega_tau_bottom
    tau = nparctan(tan_omega_tau)/(2.0*omega)

    YpY = npsum( wi*mags*mags)

    YpC = npsum( wi*mags*cos_omegat )
    YpS = npsum( wi*mags*sin_omegat )

    # SpS = npsum( wi*sin2_omegat )

    # the final terms
    YY = YpY - Y*Y
    YC = YpC - Y*C
    YS = YpS - Y*S

    periodogramvalue = (YC*YC/CC + YS*YS/SS)/YY

    return periodogramvalue