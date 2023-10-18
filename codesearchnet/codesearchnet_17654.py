def stoichiometry_coefficient(compound, element):
    """
    Determine the stoichiometry coefficient of an element in a chemical
    compound.

    :param compound: Formula of a chemical compound, e.g. 'SiO2'.
    :param element:  Element, e.g. 'Si'.

    :returns: Stoichiometry coefficient.
    """

    stoichiometry = parse_compound(compound.strip()).count()

    return stoichiometry[element]