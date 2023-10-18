def Cp(compound_string, T, mass=1.0):
    """
    Calculate the heat capacity of the compound for the specified temperature
    and mass.

    :param compound_string: Formula and phase of chemical compound, e.g.
      'Fe2O3[S1]'.
    :param T: [°C] temperature
    :param mass: [kg]

    :returns: [kWh/K] Heat capacity.
    """

    formula, phase = _split_compound_string_(compound_string)
    TK = T + 273.15
    compound = compounds[formula]
    result = compound.Cp(phase, TK)

    return _finalise_result_(compound, result, mass)