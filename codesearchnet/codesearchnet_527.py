def save_npz_dict(save_list=None, name='model.npz', sess=None):
    """Input parameters and the file name, save parameters as a dictionary into .npz file.

    Use ``tl.files.load_and_assign_npz_dict()`` to restore.

    Parameters
    ----------
    save_list : list of parameters
        A list of parameters (tensor) to be saved.
    name : str
        The name of the `.npz` file.
    sess : Session
        TensorFlow Session.

    """
    if sess is None:
        raise ValueError("session is None.")
    if save_list is None:
        save_list = []

    save_list_names = [tensor.name for tensor in save_list]
    save_list_var = sess.run(save_list)
    save_var_dict = {save_list_names[idx]: val for idx, val in enumerate(save_list_var)}
    np.savez(name, **save_var_dict)
    save_list_var = None
    save_var_dict = None
    del save_list_var
    del save_var_dict
    logging.info("[*] Model saved in npz_dict %s" % name)