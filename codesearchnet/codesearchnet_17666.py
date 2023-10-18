def _split_compound_string_(compound_string):
    """
    Split a compound's combined formula and phase into separate strings for
    the formula and phase.

    :param compound_string: Formula and phase of a chemical compound, e.g.
      'SiO2[S1]'.

    :returns: Formula of chemical compound.
    :returns: Phase of chemical compound.
    """

    formula = compound_string.replace(']', '').split('[')[0]
    phase = compound_string.replace(']', '').split('[')[1]

    return formula, phase