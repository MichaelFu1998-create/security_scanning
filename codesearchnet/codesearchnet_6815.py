def COSTALD_mixture(xs, T, Tcs, Vcs, omegas):
    r'''Calculate mixture liquid density using the COSTALD CSP method.

    A popular and accurate estimation method. If possible, fit parameters are
    used; alternatively critical properties work well.

    The mixing rules giving parameters for the pure component COSTALD
    equation are:

    .. math::
        T_{cm} = \frac{\sum_i\sum_j x_i x_j (V_{ij}T_{cij})}{V_m}

        V_m = 0.25\left[ \sum x_i V_i + 3(\sum x_i V_i^{2/3})(\sum_i x_i V_i^{1/3})\right]

        V_{ij}T_{cij} = (V_iT_{ci}V_{j}T_{cj})^{0.5}

        \omega = \sum_i z_i \omega_i

    Parameters
    ----------
    xs: list
        Mole fractions of each component
    T : float
        Temperature of fluid [K]
    Tcs : list
        Critical temperature of fluids [K]
    Vcs : list
        Critical volumes of fluids [m^3/mol].
        This parameter is alternatively a fit parameter
    omegas : list
        (ideally SRK) Acentric factor of all fluids, [-]
        This parameter is alternatively a fit parameter.

    Returns
    -------
    Vs : float
        Saturation liquid mixture volume

    Notes
    -----
    Range: 0.25 < Tr < 0.95, often said to be to 1.0
    No example has been found.
    Units are that of critical or fit constant volume.

    Examples
    --------
    >>> COSTALD_mixture([0.4576, 0.5424], 298.,  [512.58, 647.29],[0.000117, 5.6e-05], [0.559,0.344] )
    2.706588773271354e-05

    References
    ----------
    .. [1] Hankinson, Risdon W., and George H. Thomson. "A New Correlation for
       Saturated Densities of Liquids and Their Mixtures." AIChE Journal
       25, no. 4 (1979): 653-663. doi:10.1002/aic.690250412
    '''
    cmps = range(len(xs))
    if not none_and_length_check([xs, Tcs, Vcs, omegas]):
        raise Exception('Function inputs are incorrect format')
    sum1 = sum([xi*Vci for xi, Vci in zip(xs, Vcs)])
    sum2 = sum([xi*Vci**(2/3.) for xi, Vci in zip(xs, Vcs)])
    sum3 = sum([xi*Vci**(1/3.) for xi, Vci in zip(xs, Vcs)])
    Vm = 0.25*(sum1 + 3.*sum2*sum3)
    VijTcij = [[(Tcs[i]*Tcs[j]*Vcs[i]*Vcs[j])**0.5 for j in cmps] for i in cmps]
    omega = mixing_simple(xs, omegas)
    Tcm = sum([xs[i]*xs[j]*VijTcij[i][j]/Vm for j in cmps for i in cmps])
    return COSTALD(T, Tcm, Vm, omega)