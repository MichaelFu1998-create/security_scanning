def Brokaw(T, ys, mus, MWs, molecular_diameters, Stockmayers):
    r'''Calculates viscosity of a gas mixture according to
    mixing rules in [1]_.

    .. math::
        \eta_{mix} = \sum_{i=1}^n \frac{y_i \eta_i}{\sum_{j=1}^n y_j \phi_{ij}}

        \phi_{ij} = \left( \frac{\eta_i}{\eta_j} \right)^{0.5} S_{ij} A_{ij}

        A_{ij} = m_{ij} M_{ij}^{-0.5} \left[1 +
        \frac{M_{ij} - M_{ij}^{0.45}}
        {2(1+M_{ij}) + \frac{(1 + M_{ij}^{0.45}) m_{ij}^{-0.5}}{1 + m_{ij}}} \right]

        m_{ij} = \left[ \frac{4}{(1+M_{ij}^{-1})(1+M_{ij})}\right]^{0.25}

        M_{ij} = \frac{M_i}{M_j}

        S_{ij} = \frac{1 + (T_i^* T_j^*)^{0.5} + (\delta_i \delta_j/4)}
        {[1+T_i^* + (\delta_i^2/4)]^{0.5}[1+T_j^*+(\delta_j^2/4)]^{0.5}}

        T^* = kT/\epsilon

    Parameters
    ----------
    T : float
        Temperature of fluid, [K]
    ys : float
        Mole fractions of gas components
    mus : float
        Gas viscosities of all components, [Pa*S]
    MWs : float
        Molecular weights of all components, [g/mol]
    molecular_diameters : float
        L-J molecular diameter  of all components, [angstroms]
    Stockmayers : float
        L-J Stockmayer energy parameters of all components, []

    Returns
    -------
    mug : float
        Viscosity of gas mixture, [Pa*S]

    Notes
    -----
    This equation is entirely dimensionless; all dimensions cancel.
    The original source has not been reviewed.

    This is DIPPR Procedure 8D: Method for the Viscosity of Nonhydrocarbon
    Vapor Mixtures at Low Pressure (Polar and Nonpolar)

    Examples
    --------
    >>> Brokaw(308.2, [0.05, 0.95], [1.34E-5, 9.5029E-6], [64.06, 46.07], [0.42, 0.19], [347, 432])
    9.699085099801568e-06

    References
    ----------
    .. [1] Brokaw, R. S. "Predicting Transport Properties of Dilute Gases."
       Industrial & Engineering Chemistry Process Design and Development
       8, no. 2 (April 1, 1969): 240-53. doi:10.1021/i260030a015.
    .. [2] Brokaw, R. S. Viscosity of Gas Mixtures, NASA-TN-D-4496, 1968.
    .. [3] Danner, Ronald P, and Design Institute for Physical Property Data.
       Manual for Predicting Chemical Process Design Data. New York, N.Y, 1982.
    '''
    cmps = range(len(ys))
    MDs = molecular_diameters
    if not none_and_length_check([ys, mus, MWs, molecular_diameters, Stockmayers]): # check same-length inputs
        raise Exception('Function inputs are incorrect format')
    Tsts = [T/Stockmayer_i for Stockmayer_i in Stockmayers]
    Sij = [[0 for i in cmps] for j in cmps]
    Mij = [[0 for i in cmps] for j in cmps]
    mij = [[0 for i in cmps] for j in cmps]
    Aij = [[0 for i in cmps] for j in cmps]
    phiij =[[0 for i in cmps] for j in cmps]

    for i in cmps:
        for j in cmps:
            Sij[i][j] = (1+(Tsts[i]*Tsts[j])**0.5 + (MDs[i]*MDs[j])/4.)/(1 + Tsts[i] + (MDs[i]**2/4.))**0.5/(1 + Tsts[j] + (MDs[j]**2/4.))**0.5
            if MDs[i] <= 0.1 and MDs[j] <= 0.1:
                Sij[i][j] = 1
            Mij[i][j] = MWs[i]/MWs[j]
            mij[i][j] = (4./(1+Mij[i][j]**-1)/(1+Mij[i][j]))**0.25

            Aij[i][j] = mij[i][j]*Mij[i][j]**-0.5*(1 + (Mij[i][j]-Mij[i][j]**0.45)/(2*(1+Mij[i][j]) + (1+Mij[i][j]**0.45)*mij[i][j]**-0.5/(1+mij[i][j])))

            phiij[i][j] = (mus[i]/mus[j])**0.5*Sij[i][j]*Aij[i][j]

    return sum([ys[i]*mus[i]/sum([ys[j]*phiij[i][j] for j in cmps]) for i in cmps])