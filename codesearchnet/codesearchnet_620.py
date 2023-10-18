def binary_cross_entropy(output, target, epsilon=1e-8, name='bce_loss'):
    """Binary cross entropy operation.

    Parameters
    ----------
    output : Tensor
        Tensor with type of `float32` or `float64`.
    target : Tensor
        The target distribution, format the same with `output`.
    epsilon : float
        A small value to avoid output to be zero.
    name : str
        An optional name to attach to this function.

    References
    -----------
    - `ericjang-DRAW <https://github.com/ericjang/draw/blob/master/draw.py#L73>`__

    """
    #     with ops.op_scope([output, target], name, "bce_loss") as name:
    #         output = ops.convert_to_tensor(output, name="preds")
    #         target = ops.convert_to_tensor(targets, name="target")

    # with tf.name_scope(name):
    return tf.reduce_mean(
        tf.reduce_sum(-(target * tf.log(output + epsilon) + (1. - target) * tf.log(1. - output + epsilon)), axis=1),
        name=name
    )