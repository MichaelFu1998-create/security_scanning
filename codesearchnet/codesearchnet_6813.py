def Amgat(xs, Vms):
    r'''Calculate mixture liquid density using the Amgat mixing rule.
    Highly inacurate, but easy to use. Assumes idea liquids with
    no excess volume. Average molecular weight should be used with it to obtain
    density.

    .. math::
        V_{mix} = \sum_i x_i V_i

    or in terms of density:

    .. math::

        \rho_{mix} = \sum\frac{x_i}{\rho_i}

    Parameters
    ----------
    xs : array
        Mole fractions of each component, []
    Vms : array
        Molar volumes of each fluids at conditions [m^3/mol]

    Returns
    -------
    Vm : float
        Mixture liquid volume [m^3/mol]

    Notes
    -----
    Units are that of the given volumes.
    It has been suggested to use this equation with weight fractions,
    but the results have been less accurate.

    Examples
    --------
    >>> Amgat([0.5, 0.5], [4.057e-05, 5.861e-05])
    4.9590000000000005e-05
    '''
    if not none_and_length_check([xs, Vms]):
        raise Exception('Function inputs are incorrect format')
    return mixing_simple(xs, Vms)