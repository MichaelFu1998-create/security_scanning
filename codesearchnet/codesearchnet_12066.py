def aovhm_theta(times, mags, errs, frequency,
                nharmonics, magvariance):
    '''This calculates the harmonic AoV theta statistic for a frequency.

    This is a mostly faithful translation of the inner loop in `aovper.f90`. See
    the following for details:

    - http://users.camk.edu.pl/alex/
    - Schwarzenberg-Czerny (`1996
      <http://iopscience.iop.org/article/10.1086/309985/meta>`_)

    Schwarzenberg-Czerny (1996) equation 11::

        theta_prefactor = (K - 2N - 1)/(2N)
        theta_top = sum(c_n*c_n) (from n=0 to n=2N)
        theta_bot = variance(timeseries) - sum(c_n*c_n) (from n=0 to n=2N)

        theta = theta_prefactor * (theta_top/theta_bot)

        N = number of harmonics (nharmonics)
        K = length of time series (times.size)

    Parameters
    ----------

    times,mags,errs : np.array
        The input time-series to calculate the test statistic for. These should
        all be of nans/infs and be normalized to zero.

    frequency : float
        The test frequency to calculate the statistic for.

    nharmonics : int
        The number of harmonics to calculate up to.The recommended range is 4 to
        8.

    magvariance : float
        This is the (weighted by errors) variance of the magnitude time
        series. We provide it as a pre-calculated value here so we don't have to
        re-calculate it for every worker.

    Returns
    -------

    aov_harmonic_theta : float
        THe value of the harmonic AoV theta for the specified test `frequency`.

    '''

    period = 1.0/frequency

    ndet = times.size
    two_nharmonics = nharmonics + nharmonics

    # phase with test period
    phasedseries = phase_magseries_with_errs(
        times, mags, errs, period, times[0],
        sort=True, wrap=False
    )

    # get the phased quantities
    phase = phasedseries['phase']
    pmags = phasedseries['mags']
    perrs = phasedseries['errs']

    # this is sqrt(1.0/errs^2) -> the weights
    pweights = 1.0/perrs

    # multiply by 2.0*PI (for omega*time)
    phase = phase * 2.0 * pi_value

    # this is the z complex vector
    z = npcos(phase) + 1.0j*npsin(phase)

    # multiply phase with N
    phase = nharmonics * phase

    # this is the psi complex vector
    psi = pmags * pweights * (npcos(phase) + 1j*npsin(phase))

    # this is the initial value of z^n
    zn = 1.0 + 0.0j

    # this is the initial value of phi
    phi = pweights + 0.0j

    # initialize theta to zero
    theta_aov = 0.0

    # go through all the harmonics now up to 2N
    for _ in range(two_nharmonics):

        # this is <phi, phi>
        phi_dot_phi = npsum(phi * phi.conjugate())

        # this is the alpha_n numerator
        alpha = npsum(pweights * z * phi)

        # this is <phi, psi>. make sure to use npvdot and NOT npdot to get
        # complex conjugate of first vector as expected for complex vectors
        phi_dot_psi = npvdot(phi, psi)

        # make sure phi_dot_phi is not zero
        phi_dot_phi = npmax([phi_dot_phi, 10.0e-9])

        # this is the expression for alpha_n
        alpha = alpha / phi_dot_phi

        # update theta_aov for this harmonic
        theta_aov = (theta_aov +
                     npabs(phi_dot_psi) * npabs(phi_dot_psi) / phi_dot_phi)

        # use the recurrence relation to find the next phi
        phi = phi * z - alpha * zn * phi.conjugate()

        # update z^n
        zn = zn * z


    # done with all harmonics, calculate the theta_aov for this freq
    # the max below makes sure that magvariance - theta_aov > zero
    theta_aov = ( (ndet - two_nharmonics - 1.0) * theta_aov /
                  (two_nharmonics * npmax([magvariance - theta_aov,
                                           1.0e-9])) )

    return theta_aov