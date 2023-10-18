def assign_params(sess, params, network):
    """Assign the given parameters to the TensorLayer network.

    Parameters
    ----------
    sess : Session
        TensorFlow Session.
    params : list of array
        A list of parameters (array) in order.
    network : :class:`Layer`
        The network to be assigned.

    Returns
    --------
    list of operations
        A list of tf ops in order that assign params. Support sess.run(ops) manually.

    Examples
    --------
    - See ``tl.files.save_npz``

    References
    ----------
    - `Assign value to a TensorFlow variable <http://stackoverflow.com/questions/34220532/how-to-assign-value-to-a-tensorflow-variable>`__

    """
    ops = []
    for idx, param in enumerate(params):
        ops.append(network.all_params[idx].assign(param))
    if sess is not None:
        sess.run(ops)
    return ops