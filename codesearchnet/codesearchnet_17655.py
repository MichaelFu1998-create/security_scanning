def stoichiometry_coefficients(compound, elements):
    """
    Determine the stoichiometry coefficients of the specified elements in
    the specified chemical compound.

    :param compound: Formula of a chemical compound, e.g. 'SiO2'.
    :param elements: List of elements, e.g. ['Si', 'O', 'C'].

    :returns: List of stoichiometry coefficients.
    """

    stoichiometry = parse_compound(compound.strip()).count()

    return [stoichiometry[element] for element in elements]