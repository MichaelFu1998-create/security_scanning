def load_data_factsage(path=''):
    """
    Load all the thermochemical data factsage files located at a path.

    :param path: Path at which the data files are located.
    """

    compounds.clear()

    if path == '':
        path = default_data_path
    if not os.path.exists(path):
        warnings.warn('The specified data file path does not exist. (%s)' % path)
        return

    files = glob.glob(os.path.join(path, 'Compound_*.txt'))

    for file in files:
        compound = Compound(_read_compound_from_factsage_file_(file))
        compounds[compound.formula] = compound