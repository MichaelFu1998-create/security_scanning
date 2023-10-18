def load_and_assign_npz(sess=None, name=None, network=None):
    """Load model from npz and assign to a network.

    Parameters
    -------------
    sess : Session
        TensorFlow Session.
    name : str
        The name of the `.npz` file.
    network : :class:`Layer`
        The network to be assigned.

    Returns
    --------
    False or network
        Returns False, if the model is not exist.

    Examples
    --------
    - See ``tl.files.save_npz``

    """
    if network is None:
        raise ValueError("network is None.")
    if sess is None:
        raise ValueError("session is None.")
    if not os.path.exists(name):
        logging.error("file {} doesn't exist.".format(name))
        return False
    else:
        params = load_npz(name=name)
        assign_params(sess, params, network)
        logging.info("[*] Load {} SUCCESS!".format(name))
        return network