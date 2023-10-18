def leaky_twice_relu6(x, alpha_low=0.2, alpha_high=0.2, name="leaky_relu6"):
    """:func:`leaky_twice_relu6` can be used through its shortcut: :func:`:func:`tl.act.ltrelu6`.

    This activation function is a modified version :func:`leaky_relu` introduced by the following paper:
    `Rectifier Nonlinearities Improve Neural Network Acoustic Models [A. L. Maas et al., 2013] <https://ai.stanford.edu/~amaas/papers/relu_hybrid_icml2013_final.pdf>`__

    This activation function also follows the behaviour of the activation function :func:`tf.nn.relu6` introduced by the following paper:
    `Convolutional Deep Belief Networks on CIFAR-10 [A. Krizhevsky, 2010] <http://www.cs.utoronto.ca/~kriz/conv-cifar10-aug2010.pdf>`__

    This function push further the logic by adding `leaky` behaviour both below zero and above six.

    The function return the following results:
      - When x < 0: ``f(x) = alpha_low * x``.
      - When x in [0, 6]: ``f(x) = x``.
      - When x > 6: ``f(x) = 6 + (alpha_high * (x-6))``.

    Parameters
    ----------
    x : Tensor
        Support input type ``float``, ``double``, ``int32``, ``int64``, ``uint8``, ``int16``, or ``int8``.
    alpha_low : float
        Slope for x < 0: ``f(x) = alpha_low * x``.
    alpha_high : float
        Slope for x < 6: ``f(x) = 6 (alpha_high * (x-6))``.
    name : str
        The function name (optional).

    Examples
    --------
    >>> import tensorlayer as tl
    >>> net = tl.layers.DenseLayer(net, 100, act=lambda x : tl.act.leaky_twice_relu6(x, 0.2, 0.2), name='dense')

    Returns
    -------
    Tensor
        A ``Tensor`` in the same type as ``x``.

    References
    ----------
    - `Rectifier Nonlinearities Improve Neural Network Acoustic Models [A. L. Maas et al., 2013] <https://ai.stanford.edu/~amaas/papers/relu_hybrid_icml2013_final.pdf>`__
    - `Convolutional Deep Belief Networks on CIFAR-10 [A. Krizhevsky, 2010] <http://www.cs.utoronto.ca/~kriz/conv-cifar10-aug2010.pdf>`__

    """
    if not isinstance(alpha_high, tf.Tensor) and not (0 < alpha_high <= 1):
        raise ValueError("`alpha_high` value must be in [0, 1]`")

    if not isinstance(alpha_low, tf.Tensor) and not (0 < alpha_low <= 1):
        raise ValueError("`alpha_low` value must be in [0, 1]`")

    with tf.name_scope(name, "leaky_twice_relu6") as name_scope:
        x = tf.convert_to_tensor(x, name="features")

        x_is_above_0 = tf.minimum(x, 6 * (1 - alpha_high) + alpha_high * x)
        x_is_below_0 = tf.minimum(alpha_low * x, 0)

        return tf.maximum(x_is_above_0, x_is_below_0, name=name_scope)