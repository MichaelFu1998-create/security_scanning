def Bahadori_gas(T, MW):
    r'''Estimates the thermal conductivity of hydrocarbons gases at low P.
    Fits their data well, and is useful as only MW is required.
    Y is the Molecular weight, and X the temperature.

    .. math::
        K = a + bY + CY^2 + dY^3

        a = A_1 + B_1 X + C_1 X^2 + D_1 X^3

        b = A_2 + B_2 X + C_2 X^2 + D_2 X^3

        c = A_3 + B_3 X + C_3 X^2 + D_3 X^3

        d = A_4 + B_4 X + C_4 X^2 + D_4 X^3

    Parameters
    ----------
    T : float
        Temperature of the gas [K]
    MW : float
        Molecular weight of the gas [g/mol]

    Returns
    -------
    kg : float
        Estimated gas thermal conductivity [W/m/k]

    Notes
    -----
    The accuracy of this equation has not been reviewed.

    Examples
    --------
    >>> Bahadori_gas(40+273.15, 20) # Point from article
    0.031968165337873326

    References
    ----------
    .. [1] Bahadori, Alireza, and Saeid Mokhatab. "Estimating Thermal
       Conductivity of Hydrocarbons." Chemical Engineering 115, no. 13
       (December 2008): 52-54
    '''
    A = [4.3931323468E-1, -3.88001122207E-2, 9.28616040136E-4, -6.57828995724E-6]
    B = [-2.9624238519E-3, 2.67956145820E-4, -6.40171884139E-6, 4.48579040207E-8]
    C = [7.54249790107E-6, -6.46636219509E-7, 1.5124510261E-8, -1.0376480449E-10]
    D = [-6.0988433456E-9, 5.20752132076E-10, -1.19425545729E-11, 8.0136464085E-14]
    X, Y = T, MW
    a = A[0] + B[0]*X + C[0]*X**2 + D[0]*X**3
    b = A[1] + B[1]*X + C[1]*X**2 + D[1]*X**3
    c = A[2] + B[2]*X + C[2]*X**2 + D[2]*X**3
    d = A[3] + B[3]*X + C[3]*X**2 + D[3]*X**3
    return a + b*Y + c*Y**2 + d*Y**3