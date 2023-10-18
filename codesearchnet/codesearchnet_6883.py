def Diguilio_Teja(T, xs, sigmas_Tb, Tbs, Tcs):
    r'''Calculates surface tension of a liquid mixture according to
    mixing rules in [1]_.

    .. math::
        \sigma = 1.002855(T^*)^{1.118091} \frac{T}{T_b} \sigma_r

        T^*  = \frac{(T_c/T)-1}{(T_c/T_b)-1}

        \sigma_r = \sum x_i \sigma_i

        T_b = \sum x_i T_{b,i}

        T_c = \sum x_i T_{c,i}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    xs : array-like
        Mole fractions of all components
    sigmas_Tb : array-like
        Surface tensions of all components at the boiling point, [N/m]
    Tbs : array-like
        Boiling temperatures of all components, [K]
    Tcs : array-like
        Critical temperatures of all components, [K]

    Returns
    -------
    sigma : float
        Air-liquid surface tension of mixture, [N/m]

    Notes
    -----
    Simple model, however it has 0 citations. Gives similar results to the
    `Winterfeld_Scriven_Davis` model.

    Raises a ValueError if temperature is greater than the mixture's critical
    temperature or if the given temperature is negative, or if the mixture's
    boiling temperature is higher than its critical temperature.
    
    [1]_ claims a 4.63 percent average absolute error on 21 binary and 4 
    ternary non-aqueous systems. [1]_ also considered Van der Waals mixing 
    rules for `Tc`, but found it provided a higher error of 5.58%

    Examples
    --------
    >>> Diguilio_Teja(T=298.15, xs=[0.1606, 0.8394],
    ... sigmas_Tb=[0.01424, 0.02530], Tbs=[309.21, 312.95], Tcs=[469.7, 508.0])
    0.025716823875045505

    References
    ----------
    .. [1] Diguilio, Ralph, and Amyn S. Teja. "Correlation and Prediction of
       the Surface Tensions of Mixtures." The Chemical Engineering Journal 38,
       no. 3 (July 1988): 205-8. doi:10.1016/0300-9467(88)80079-0.
    '''
    if not none_and_length_check([xs, sigmas_Tb, Tbs, Tcs]):
        raise Exception('Function inputs are incorrect format')

    Tc = mixing_simple(xs, Tcs)
    if T > Tc:
        raise ValueError('T > Tc according to Kays rule - model is not valid in this range.')
    Tb = mixing_simple(xs, Tbs)
    sigmar = mixing_simple(xs, sigmas_Tb)
    Tst = (Tc/T - 1.)/(Tc/Tb - 1)
    return 1.002855*Tst**1.118091*(T/Tb)*sigmar