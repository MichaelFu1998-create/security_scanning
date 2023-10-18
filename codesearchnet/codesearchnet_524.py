def load_npz(path='', name='model.npz'):
    """Load the parameters of a Model saved by tl.files.save_npz().

    Parameters
    ----------
    path : str
        Folder path to `.npz` file.
    name : str
        The name of the `.npz` file.

    Returns
    --------
    list of array
        A list of parameters in order.

    Examples
    --------
    - See ``tl.files.save_npz``

    References
    ----------
    - `Saving dictionary using numpy <http://stackoverflow.com/questions/22315595/saving-dictionary-of-header-information-using-numpy-savez>`__

    """
    d = np.load(os.path.join(path, name))
    return d['params']