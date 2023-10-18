def mass_fractions(amounts):
    """
    Calculate the mole fractions from the specified compound amounts.

    :param amounts: [kmol] dictionary, e.g. {'SiO2': 3.0, 'FeO': 1.5}

    :returns: [mass fractions] dictionary
    """

    m = masses(amounts)
    m_total = sum(m.values())
    return {compound: m[compound]/m_total for compound in m.keys()}