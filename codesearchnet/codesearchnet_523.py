def save_npz(save_list=None, name='model.npz', sess=None):
    """Input parameters and the file name, save parameters into .npz file. Use tl.utils.load_npz() to restore.

    Parameters
    ----------
    save_list : list of tensor
        A list of parameters (tensor) to be saved.
    name : str
        The name of the `.npz` file.
    sess : None or Session
        Session may be required in some case.

    Examples
    --------
    Save model to npz

    >>> tl.files.save_npz(network.all_params, name='model.npz', sess=sess)

    Load model from npz (Method 1)

    >>> load_params = tl.files.load_npz(name='model.npz')
    >>> tl.files.assign_params(sess, load_params, network)

    Load model from npz (Method 2)

    >>> tl.files.load_and_assign_npz(sess=sess, name='model.npz', network=network)

    Notes
    -----
    If you got session issues, you can change the value.eval() to value.eval(session=sess)

    References
    ----------
    `Saving dictionary using numpy <http://stackoverflow.com/questions/22315595/saving-dictionary-of-header-information-using-numpy-savez>`__

    """
    logging.info("[*] Saving TL params into %s" % name)
    if save_list is None:
        save_list = []

    save_list_var = []
    if sess:
        save_list_var = sess.run(save_list)
    else:
        try:
            save_list_var.extend([v.eval() for v in save_list])
        except Exception:
            logging.info(
                " Fail to save model, Hint: pass the session into this function, tl.files.save_npz(network.all_params, name='model.npz', sess=sess)"
            )
    np.savez(name, params=save_list_var)
    save_list_var = None
    del save_list_var
    logging.info("[*] Saved")