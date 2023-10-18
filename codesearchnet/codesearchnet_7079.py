def Bahadori_liquid(T, M):
    r'''Estimates the thermal conductivity of parafin liquid hydrocarbons.
    Fits their data well, and is useful as only MW is required.
    X is the Molecular weight, and Y the temperature.

    .. math::
        K = a + bY + CY^2 + dY^3

        a = A_1 + B_1 X + C_1 X^2 + D_1 X^3

        b = A_2 + B_2 X + C_2 X^2 + D_2 X^3

        c = A_3 + B_3 X + C_3 X^2 + D_3 X^3

        d = A_4 + B_4 X + C_4 X^2 + D_4 X^3

    Parameters
    ----------
    T : float
        Temperature of the fluid [K]
    M : float
        Molecular weight of the fluid [g/mol]

    Returns
    -------
    kl : float
        Estimated liquid thermal conductivity [W/m/k]

    Notes
    -----
    The accuracy of this equation has not been reviewed.

    Examples
    --------
    Data point from [1]_.

    >>> Bahadori_liquid(273.15, 170)
    0.14274278108272603

    References
    ----------
    .. [1] Bahadori, Alireza, and Saeid Mokhatab. "Estimating Thermal
       Conductivity of Hydrocarbons." Chemical Engineering 115, no. 13
       (December 2008): 52-54
    '''
    A = [-6.48326E-2, 2.715015E-3, -1.08580E-5, 9.853917E-9]
    B = [1.565612E-2, -1.55833E-4, 5.051114E-7, -4.68030E-10]
    C = [-1.80304E-4, 1.758693E-6, -5.55224E-9, 5.201365E-12]
    D = [5.880443E-7, -5.65898E-9, 1.764384E-11, -1.65944E-14]
    X, Y = M, T
    a = A[0] + B[0]*X + C[0]*X**2 + D[0]*X**3
    b = A[1] + B[1]*X + C[1]*X**2 + D[1]*X**3
    c = A[2] + B[2]*X + C[2]*X**2 + D[2]*X**3
    d = A[3] + B[3]*X + C[3]*X**2 + D[3]*X**3
    return a + b*Y + c*Y**2 + d*Y**3