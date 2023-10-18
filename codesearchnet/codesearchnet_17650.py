def convert_compound(mass, source, target, element):
    """
    Convert the specified mass of the source compound to the target using
    element as basis.

    :param mass: Mass of from_compound. [kg]
    :param source: Formula and phase of the original compound, e.g.
      'Fe2O3[S1]'.
    :param target: Formula and phase of the target compound, e.g. 'Fe[S1]'.
    :param element: Element to use as basis for the conversion, e.g. 'Fe' or
      'O'.

    :returns: Mass of target. [kg]
    """

    # Perform the conversion.
    target_mass_fraction = element_mass_fraction(target, element)
    if target_mass_fraction == 0.0:
        # If target_formula does not contain element, just return 0.0.
        return 0.0
    else:
        source_mass_fraction = element_mass_fraction(source, element)
        return mass * source_mass_fraction / target_mass_fraction