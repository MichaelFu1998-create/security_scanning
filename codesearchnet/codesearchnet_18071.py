def load(filename):
    """
    Load the state from the given file, moving to the file's directory during
    load (temporarily, moving back after loaded)

    Parameters
    ----------
    filename : string
        name of the file to open, should be a .pkl file
    """
    path, name = os.path.split(filename)
    path = path or '.'

    with util.indir(path):
        return pickle.load(open(name, 'rb'))