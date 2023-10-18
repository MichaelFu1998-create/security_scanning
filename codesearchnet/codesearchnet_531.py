def load_npy_to_any(path='', name='file.npy'):
    """Load `.npy` file.

    Parameters
    ------------
    path : str
        Path to the file (optional).
    name : str
        File name.

    Examples
    ---------
    - see tl.files.save_any_to_npy()

    """
    file_path = os.path.join(path, name)
    try:
        return np.load(file_path).item()
    except Exception:
        return np.load(file_path)
    raise Exception("[!] Fail to load %s" % file_path)