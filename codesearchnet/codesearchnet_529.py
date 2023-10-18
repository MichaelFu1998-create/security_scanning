def save_ckpt(
        sess=None, mode_name='model.ckpt', save_dir='checkpoint', var_list=None, global_step=None, printable=False
):
    """Save parameters into `ckpt` file.

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
    global_step : int or None
        Step number.
    printable : boolean
        Whether to print all parameters information.

    See Also
    --------
    load_ckpt

    """
    if sess is None:
        raise ValueError("session is None.")
    if var_list is None:
        var_list = []

    ckpt_file = os.path.join(save_dir, mode_name)
    if var_list == []:
        var_list = tf.global_variables()

    logging.info("[*] save %s n_params: %d" % (ckpt_file, len(var_list)))

    if printable:
        for idx, v in enumerate(var_list):
            logging.info("  param {:3}: {:15}   {}".format(idx, v.name, str(v.get_shape())))

    saver = tf.train.Saver(var_list)
    saver.save(sess, ckpt_file, global_step=global_step)