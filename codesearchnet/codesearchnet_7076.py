def Gharagheizi_liquid(T, M, Tb, Pc, omega):
    r'''Estimates the thermal conductivity of a liquid as a function of
    temperature using the CSP method of Gharagheizi [1]_. A  convoluted
    method claiming high-accuracy and using only statistically significant
    variable following analalysis.

    Requires temperature, molecular weight, boiling temperature and critical
    pressure and acentric factor.

    .. math::
        &k = 10^{-4}\left[10\omega + 2P_c-2T+4+1.908(T_b+\frac{1.009B^2}{MW^2})
        +\frac{3.9287MW^4}{B^4}+\frac{A}{B^8}\right]

        &A = 3.8588MW^8(1.0045B+6.5152MW-8.9756)

        &B = 16.0407MW+2T_b-27.9074

    Parameters
    ----------
    T : float
        Temperature of the fluid [K]
    M : float
        Molecular weight of the fluid [g/mol]
    Tb : float
        Boiling temperature of the fluid [K]
    Pc : float
        Critical pressure of the fluid [Pa]
    omega : float
        Acentric factor of the fluid [-]

    Returns
    -------
    kl : float
        Estimated liquid thermal conductivity [W/m/k]

    Notes
    -----
    Pressure is internally converted into bar, as used in the original equation.

    This equation was derived with 19000 points representing 1640 unique compounds.

    Examples
    --------
    >>> Gharagheizi_liquid(300, 40, 350, 1E6, 0.27)
    0.2171113029534838

    References
    ----------
    .. [1] Gharagheizi, Farhad, Poorandokht Ilani-Kashkouli, Mehdi Sattari,
        Amir H. Mohammadi, Deresh Ramjugernath, and Dominique Richon.
        "Development of a General Model for Determination of Thermal
        Conductivity of Liquid Chemical Compounds at Atmospheric Pressure."
        AIChE Journal 59, no. 5 (May 1, 2013): 1702-8. doi:10.1002/aic.13938
    '''
    Pc = Pc/1E5
    B = 16.0407*M + 2.*Tb - 27.9074
    A = 3.8588*M**8*(1.0045*B + 6.5152*M - 8.9756)
    kl = 1E-4*(10.*omega + 2.*Pc - 2.*T + 4. + 1.908*(Tb + 1.009*B*B/(M*M))
        + 3.9287*M**4*B**-4 + A*B**-8)
    return kl