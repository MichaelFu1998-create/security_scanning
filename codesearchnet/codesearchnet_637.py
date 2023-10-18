def swish(x, name='swish'):
    """Swish function.

     See `Swish: a Self-Gated Activation Function <https://arxiv.org/abs/1710.05941>`__.

    Parameters
    ----------
    x : Tensor
        input.
    name: str
        function name (optional).

    Returns
    -------
    Tensor
        A ``Tensor`` in the same type as ``x``.

    """
    with tf.name_scope(name):
        x = tf.nn.sigmoid(x) * x
    return x