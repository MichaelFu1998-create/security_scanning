def ITS90_68_difference(T):
    r'''Calculates the difference between ITS-90 and ITS-68 scales using a
    series of models listed in [1]_, [2]_, and [3]_.

    The temperature difference is given by the following equations:

    From 13.8 K to 73.15 K:

    .. math::
        T_{90} - T_{68} = a_0 + \sum_{i=1}^{12} a_i[(T_{90}/K-40)/40]^i

    From 83.8 K to 903.75 K:

    .. math::
        T_{90} - T_{68} = \sum_{i=1}^8 b_i[(T_{90}/K - 273.15)/630]^i

    From 903.75 K to 1337.33 K:

    .. math::
        T_{90} - T_{68} = \sum_{i=0}^5 c_i[T_{90}/^\circ C]^i

    Above 1337.33 K:

    .. math::
        T_{90} - T_{68} = -1.398\cdot 10^{-7}\left(\frac{T_{90}}{K}\right)^2


    Parameters
    ----------
    T : float
        Temperature, ITS-90, or approximately ITS-68 [K]

    Returns
    -------
    dT : float
        Temperature, difference between ITS-90 and ITS-68 at T [K]

    Notes
    -----
    The conversion is straightforward when T90 is known. Theoretically, the
    model should be solved numerically to convert the reverse way. However,
    according to [4]_, the difference is under 0.05 mK from 73.15 K to
    903.15 K, and under 0.26 mK up to 1337.33 K.

    For temperatures under 13.8 K, no conversion is performed.

    The first set of coefficients are:
    -0.005903, 0.008174, -0.061924, -0.193388, 1.490793, 1.252347, -9.835868,
    1.411912, 25.277595, -19.183815, -18.437089, 27.000895, -8.716324.

    The second set of coefficients are:
    0, -0.148759, -0.267408, 1.08076, 1.269056, -4.089591, -1.871251,
    7.438081, -3.536296.

    The third set of coefficients are:
    7.8687209E1, -4.7135991E-1, 1.0954715E-3, -1.2357884E-6, 6.7736583E-10,
    -1.4458081E-13.
    These last coefficients use the temperature in degrees Celcius. A slightly
    older model used the following coefficients but a different equation over
    the same range:
    -0.00317, -0.97737, 1.2559, 2.03295, -5.91887, -3.23561, 7.23364,
    5.04151. The model for these coefficients was:

    .. math::
        T_{90} - T_{68} = c_0 + \sum_{i=1}^7 c_i[(T_{90}/K - 1173.15)/300]^i

    For temperatures larger than several thousand K, the differences have no
    meaning and grows quadratically.

    Examples
    --------
    >>> ITS90_68_difference(1000.)
    0.01231818956580355

    References
    ----------
    .. [1] Bedford, R. E., G. Bonnier, H. Maas, and F. Pavese. "Techniques for
       Approximating the International Temperature Scale of 1990." Bureau
       International Des Poids et Mesures, Sfievres, 1990.
    .. [2] Wier, Ron D., and Robert N. Goldberg. "On the Conversion of
       Thermodynamic Properties to the Basis of the International Temperature
       Scale of 1990." The Journal of Chemical Thermodynamics 28, no. 3
       (March 1996): 261-76. doi:10.1006/jcht.1996.0026.
    .. [3] Goldberg, Robert N., and R. D. Weir. "Conversion of Temperatures
       and Thermodynamic Properties to the Basis of the International
       Temperature Scale of 1990 (Technical Report)." Pure and Applied
       Chemistry 64, no. 10 (1992): 1545-1562. doi:10.1351/pac199264101545.
    .. [4] Code10.info. "Conversions among International Temperature Scales."
       Accessed May 22, 2016. http://www.code10.info/index.php%3Foption%3Dcom_content%26view%3Darticle%26id%3D83:conversions-among-international-temperature-scales%26catid%3D60:temperature%26Itemid%3D83.
    '''
    ais = [-0.005903, 0.008174, -0.061924, -0.193388, 1.490793, 1.252347,
           -9.835868, 1.411912, 25.277595, -19.183815, -18.437089, 27.000895,
           -8.716324]
    bis = [0, -0.148759, -0.267408, 1.08076, 1.269056, -4.089591, -1.871251,
           7.438081, -3.536296]
#    cis = [-0.00317, -0.97737, 1.2559, 2.03295, -5.91887, -3.23561, 7.23364,
#           5.04151]
    new_cs = [7.8687209E1, -4.7135991E-1, 1.0954715E-3, -1.2357884E-6,
              6.7736583E-10, -1.4458081E-13]
    dT = 0
    if T < 13.8:
        dT = 0
    elif T >= 13.8 and T <= 73.15:
        for i in range(13):
            dT += ais[i]*((T - 40.)/40.)**i
    elif T > 73.15 and T < 83.8:
        dT = 0
    elif T >= 83.8 and T <= 903.75:
        for i in range(9):
            dT += bis[i]*((T - 273.15)/630.)**i
    elif T > 903.75 and T <= 1337.33:
        # Revised function exists, but does not match the tabulated data
        # for i in range(8):
        #    dT += cis[i]*((T - 1173.15)/300.)**i
        for i in range(6):
            dT += new_cs[i]*(T-273.15)**i
    elif T > 1337.33:
        dT = -1.398E-7*T**2

    return dT