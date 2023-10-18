def molar_mass(compound=''):
    """Determine the molar mass of a chemical compound.

    The molar mass is usually the mass of one mole of the substance, but here
    it is the mass of 1000 moles, since the mass unit used in auxi is kg.

    :param compound: Formula of a chemical compound, e.g. 'Fe2O3'.

    :returns: Molar mass. [kg/kmol]
    """

    result = 0.0
    if compound is None or len(compound) == 0:
        return result

    compound = compound.strip()

    parsed = parse_compound(compound)

    return parsed.molar_mass()