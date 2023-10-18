def leaky_relu(x, alpha=0.2, name="leaky_relu"):
    """leaky_relu can be used through its shortcut: :func:`tl.act.lrelu`.

    This function is a modified version of ReLU, introducing a nonzero gradient for negative input. Introduced by the paper:
    `Rectifier Nonlinearities Improve Neural Network Acoustic Models [A. L. Maas et al., 2013] <https://ai.stanford.edu/~amaas/papers/relu_hybrid_icml2013_final.pdf>`__

    The function return the following results:
      - When x < 0: ``f(x) = alpha_low * x``.
      - When x >= 0: ``f(x) = x``.

    Parameters
    ----------
    x : Tensor
        Support input type ``float``, ``double``, ``int32``, ``int64``, ``uint8``, ``int16``, or ``int8``.
    alpha : float
        Slope.
    name : str
        The function name (optional).

    Examples
    --------
    >>> import tensorlayer as tl
    >>> net = tl.layers.DenseLayer(net, 100, act=lambda x : tl.act.lrelu(x, 0.2), name='dense')

    Returns
    -------
    Tensor
        A ``Tensor`` in the same type as ``x``.

    References
    ----------
    - `Rectifier Nonlinearities Improve Neural Network Acoustic Models [A. L. Maas et al., 2013] <https://ai.stanford.edu/~amaas/papers/relu_hybrid_icml2013_final.pdf>`__

    """
    if not (0 < alpha <= 1):
        raise ValueError("`alpha` value must be in [0, 1]`")

    with tf.name_scope(name, "leaky_relu") as name_scope:
        x = tf.convert_to_tensor(x, name="features")
        return tf.maximum(x, alpha * x, name=name_scope)