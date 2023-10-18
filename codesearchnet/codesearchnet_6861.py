def thermal_conductivity_Magomedov(T, P, ws, CASRNs, k_w=None):
    r'''Calculate the thermal conductivity of an aqueous mixture of
    electrolytes using the form proposed by Magomedov [1]_.
    Parameters are loaded by the function as needed. Function will fail if an
    electrolyte is not in the database.

    .. math::
        \lambda = \lambda_w\left[ 1 - \sum_{i=1}^n A_i (w_i + 2\times10^{-4}
        w_i^3)\right] - 2\times10^{-8} PT\sum_{i=1}^n w_i

    Parameters
    ----------
    T : float
        Temperature of liquid [K]
    P : float
        Pressure of the liquid [Pa]
    ws : array
        Weight fractions of liquid components other than water
    CASRNs : array
        CAS numbers of the liquid components other than water
    k_w : float
        Liquid thermal condiuctivity or pure water at T and P, [W/m/K]

    Returns
    -------
    kl : float
        Liquid thermal condiuctivity, [W/m/K]

    Notes
    -----
    Range from 273 K to 473 K, P from 0.1 MPa to 100 MPa. C from 0 to 25 mass%.
    Internal untis are MPa for pressure and weight percent.

    An example is sought for this function. It is not possible to reproduce
    the author's values consistently.

    Examples
    --------
    >>> thermal_conductivity_Magomedov(293., 1E6, [.25], ['7758-94-3'], k_w=0.59827)
    0.548654049375

    References
    ----------
    .. [1] Magomedov, U. B. "The Thermal Conductivity of Binary and
       Multicomponent Aqueous Solutions of Inorganic Substances at High
       Parameters of State." High Temperature 39, no. 2 (March 1, 2001):
       221-26. doi:10.1023/A:1017518731726.
    '''
    P = P/1E6
    ws = [i*100 for i in ws]
    if not k_w:
        raise Exception('k_w correlation must be provided')

    sum1 = 0
    for i, CASRN in enumerate(CASRNs):
        Ai = float(Magomedovk_thermal_cond.at[CASRN, 'Ai'])
        sum1 += Ai*(ws[i] + 2E-4*ws[i]**3)
    return k_w*(1 - sum1) - 2E-8*P*T*sum(ws)