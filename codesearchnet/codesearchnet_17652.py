def elements(compounds):
    """
    Determine the set of elements present in a list of chemical compounds.

    The list of elements is sorted alphabetically.

    :param compounds: List of compound formulas and phases, e.g.
      ['Fe2O3[S1]', 'Al2O3[S1]'].

    :returns: List of elements.
    """

    elementlist = [parse_compound(compound).count().keys()
                   for compound in compounds]
    return set().union(*elementlist)