def load_ckpt(sess=None, mode_name='model.ckpt', save_dir='checkpoint', var_list=None, is_latest=True, printable=False):
    """Load parameters from `ckpt` file.

    Parameters
    ------------
    sess : Session
        TensorFlow Session.
    mode_name : str
        The name of the model, default is ``model.ckpt``.
    save_dir : str
        The path / file directory to the `ckpt`, default is ``checkpoint``.
    var_list : list of tensor
        The parameters / variables (tensor) to be saved. If empty, save all global variables (default).
    is_latest : boolean
        Whether to load the latest `ckpt`, if False, load the `ckpt` with the name of ```mode_name``.
    printable : boolean
        Whether to print all parameters information.

    Examples
    ----------
    - Save all global parameters.

    >>> tl.files.save_ckpt(sess=sess, mode_name='model.ckpt', save_dir='model', printable=True)

    - Save specific parameters.

    >>> tl.files.save_ckpt(sess=sess, mode_name='model.ckpt', var_list=net.all_params, save_dir='model', printable=True)

    - Load latest ckpt.

    >>> tl.files.load_ckpt(sess=sess, var_list=net.all_params, save_dir='model', printable=True)

    - Load specific ckpt.

    >>> tl.files.load_ckpt(sess=sess, mode_name='model.ckpt', var_list=net.all_params, save_dir='model', is_latest=False, printable=True)

    """
    if sess is None:
        raise ValueError("session is None.")
    if var_list is None:
        var_list = []

    if is_latest:
        ckpt_file = tf.train.latest_checkpoint(save_dir)
    else:
        ckpt_file = os.path.join(save_dir, mode_name)

    if not var_list:
        var_list = tf.global_variables()

    logging.info("[*] load %s n_params: %d" % (ckpt_file, len(var_list)))

    if printable:
        for idx, v in enumerate(var_list):
            logging.info("  param {:3}: {:15}   {}".format(idx, v.name, str(v.get_shape())))

    try:
        saver = tf.train.Saver(var_list)
        saver.restore(sess, ckpt_file)
    except Exception as e:
        logging.info(e)
        logging.info("[*] load ckpt fail ...")