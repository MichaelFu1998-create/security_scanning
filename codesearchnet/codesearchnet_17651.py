def element_mass_fraction(compound, element):
    """
    Determine the mass fraction of an element in a chemical compound.

    :param compound: Formula of the chemical compound, 'FeCr2O4'.
    :param element: Element, e.g. 'Cr'.

    :returns: Element mass fraction.
    """

    coeff = stoichiometry_coefficient(compound, element)

    if coeff == 0.0:
        return 0.0

    formula_mass = molar_mass(compound)
    element_mass = molar_mass(element)
    return coeff * element_mass / formula_mass