def ramp(x, v_min=0, v_max=1, name=None):
    """Ramp activation function.

    Parameters
    ----------
    x : Tensor
        input.
    v_min : float
        cap input to v_min as a lower bound.
    v_max : float
        cap input to v_max as a upper bound.
    name : str
        The function name (optional).

    Returns
    -------
    Tensor
        A ``Tensor`` in the same type as ``x``.

    """
    return tf.clip_by_value(x, clip_value_min=v_min, clip_value_max=v_max, name=name)