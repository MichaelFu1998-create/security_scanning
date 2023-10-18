def list_compounds():
    """
    List all compounds that are currently loaded in the thermo module, and
    their phases.
    """

    print('Compounds currently loaded:')
    for compound in sorted(compounds.keys()):
        phases = compounds[compound].get_phase_list()
        print('%s: %s' % (compound, ', '.join(phases)))