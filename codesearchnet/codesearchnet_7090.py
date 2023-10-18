def Gharagheizi_gas(T, MW, Tb, Pc, omega):
    r'''Estimates the thermal conductivity of a gas as a function of
    temperature using the CSP method of Gharagheizi [1]_. A  convoluted
    method claiming high-accuracy and using only statistically significant
    variable following analalysis.

    Requires temperature, molecular weight, boiling temperature and critical
    pressure and acentric factor.

    .. math::
        k = 7.9505\times 10^{-4} + 3.989\times 10^{-5} T
        -5.419\times 10^-5 M + 3.989\times 10^{-5} A

       A = \frac{\left(2\omega + T - \frac{(2\omega + 3.2825)T}{T_b} + 3.2825\right)}{0.1MP_cT}
        \times (3.9752\omega + 0.1 P_c + 1.9876B + 6.5243)^2


    Parameters
    ----------
    T : float
        Temperature of the fluid [K]
    MW: float
        Molecular weight of the fluid [g/mol]
    Tb : float
        Boiling temperature of the fluid [K]
    Pc : float
        Critical pressure of the fluid [Pa]
    omega : float
        Acentric factor of the fluid [-]

    Returns
    -------
    kg : float
        Estimated gas thermal conductivity [W/m/k]

    Notes
    -----
    Pressure is internally converted into 10*kPa but author used correlation with
    kPa; overall, errors have been corrected in the presentation of the formula.

    This equation was derived with 15927 points and 1574 compounds.
    Example value from [1]_ is the first point in the supportinf info, for CH4.

    Examples
    --------
    >>> Gharagheizi_gas(580., 16.04246, 111.66, 4599000.0, 0.0115478000)
    0.09594861261873211

    References
    ----------
    .. [1] Gharagheizi, Farhad, Poorandokht Ilani-Kashkouli, Mehdi Sattari,
       Amir H. Mohammadi, Deresh Ramjugernath, and Dominique Richon.
       "Development of a General Model for Determination of Thermal
       Conductivity of Liquid Chemical Compounds at Atmospheric Pressure."
       AIChE Journal 59, no. 5 (May 1, 2013): 1702-8. doi:10.1002/aic.13938
    '''
    Pc = Pc/1E4
    B = T + (2.*omega + 2.*T - 2.*T*(2.*omega + 3.2825)/Tb + 3.2825)/(2*omega + T - T*(2*omega+3.2825)/Tb + 3.2825) - T*(2*omega+3.2825)/Tb
    A = (2*omega + T - T*(2*omega + 3.2825)/Tb + 3.2825)/(0.1*MW*Pc*T) * (3.9752*omega + 0.1*Pc + 1.9876*B + 6.5243)**2
    return 7.9505E-4 + 3.989E-5*T - 5.419E-5*MW + 3.989E-5*A