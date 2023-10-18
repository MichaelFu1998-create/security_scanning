def Li(zs, Tcs, Vcs):
    r'''Calculates critical temperature of a mixture according to
    mixing rules in [1]_. Better than simple mixing rules.

    .. math::
        T_{cm} = \sum_{i=1}^n \Phi_i T_{ci}\\
        \Phi = \frac{x_i V_{ci}}{\sum_{j=1}^n x_j V_{cj}}

    Parameters
    ----------
    zs : array-like
        Mole fractions of all components
    Tcs : array-like
        Critical temperatures of all components, [K]
    Vcs : array-like
        Critical volumes of all components, [m^3/mol]

    Returns
    -------
    Tcm : float
        Critical temperatures of the mixture, [K]

    Notes
    -----
    Reviewed in many papers on critical mixture temperature.

    Second example is from Najafi (2015), for ethylene, Benzene, ethylbenzene.
    This is similar to but not identical to the result from the article. The
    experimental point is 486.9 K.

    2rd example is from Najafi (2015), for:
    butane/pentane/hexane 0.6449/0.2359/0.1192 mixture, exp: 450.22 K.
    Its result is identical to that calculated in the article.

    Examples
    --------
    Nitrogen-Argon 50/50 mixture

    >>> Li([0.5, 0.5], [126.2, 150.8], [8.95e-05, 7.49e-05])
    137.40766423357667

    butane/pentane/hexane 0.6449/0.2359/0.1192 mixture, exp: 450.22 K.

    >>> Li([0.6449, 0.2359, 0.1192], [425.12, 469.7, 507.6],
    ... [0.000255, 0.000313, 0.000371])
    449.68261498555444

    References
    ----------
    .. [1] Li, C. C. "Critical Temperature Estimation for Simple Mixtures."
       The Canadian Journal of Chemical Engineering 49, no. 5
       (October 1, 1971): 709-10. doi:10.1002/cjce.5450490529.
    '''
    if not none_and_length_check([zs, Tcs, Vcs]):
        raise Exception('Function inputs are incorrect format')

    denominator = sum(zs[i]*Vcs[i] for i in range(len(zs)))
    Tcm = 0
    for i in range(len(zs)):
        Tcm += zs[i]*Vcs[i]*Tcs[i]/denominator
    return Tcm