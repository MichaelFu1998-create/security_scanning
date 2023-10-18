def get_variables_with_name(name=None, train_only=True, verbose=False):
    """Get a list of TensorFlow variables by a given name scope.

    Parameters
    ----------
    name : str
        Get the variables that contain this name.
    train_only : boolean
        If Ture, only get the trainable variables.
    verbose : boolean
        If True, print the information of all variables.

    Returns
    -------
    list of Tensor
        A list of TensorFlow variables

    Examples
    --------
    >>> import tensorlayer as tl
    >>> dense_vars = tl.layers.get_variables_with_name('dense', True, True)

    """
    if name is None:
        raise Exception("please input a name")

    logging.info("  [*] geting variables with %s" % name)

    # tvar = tf.trainable_variables() if train_only else tf.all_variables()
    if train_only:
        t_vars = tf.trainable_variables()

    else:
        t_vars = tf.global_variables()

    d_vars = [var for var in t_vars if name in var.name]

    if verbose:
        for idx, v in enumerate(d_vars):
            logging.info("  got {:3}: {:15}   {}".format(idx, v.name, str(v.get_shape())))

    return d_vars