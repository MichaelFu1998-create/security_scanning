def amount_fractions(masses):
    """
    Calculate the mole fractions from the specified compound masses.

    :param masses: [kg] dictionary, e.g. {'SiO2': 3.0, 'FeO': 1.5}

    :returns: [mole fractions] dictionary
    """

    n = amounts(masses)
    n_total = sum(n.values())
    return {compound: n[compound]/n_total for compound in n.keys()}