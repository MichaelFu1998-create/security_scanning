def masses(amounts):
    """
    Calculate the masses from the specified compound amounts.

    :param masses: [kmol] dictionary, e.g. {'SiO2': 3.0, 'FeO': 1.5}

    :returns: [kg] dictionary
    """

    return {compound: mass(compound, amounts[compound])
            for compound in amounts.keys()}