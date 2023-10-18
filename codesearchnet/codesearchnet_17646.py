def amounts(masses):
    """
    Calculate the amounts from the specified compound masses.

    :param masses: [kg] dictionary, e.g. {'SiO2': 3.0, 'FeO': 1.5}

    :returns: [kmol] dictionary
    """

    return {compound: amount(compound, masses[compound])
            for compound in masses.keys()}