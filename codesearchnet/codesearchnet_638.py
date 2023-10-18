def pixel_wise_softmax(x, name='pixel_wise_softmax'):
    """Return the softmax outputs of images, every pixels have multiple label, the sum of a pixel is 1.

    Usually be used for image segmentation.

    Parameters
    ----------
    x : Tensor
        input.
            - For 2d image, 4D tensor (batch_size, height, weight, channel), where channel >= 2.
            - For 3d image, 5D tensor (batch_size, depth, height, weight, channel), where channel >= 2.
    name : str
        function name (optional)

    Returns
    -------
    Tensor
        A ``Tensor`` in the same type as ``x``.

    Examples
    --------
    >>> outputs = pixel_wise_softmax(network.outputs)
    >>> dice_loss = 1 - dice_coe(outputs, y_, epsilon=1e-5)

    References
    ----------
    - `tf.reverse <https://www.tensorflow.org/versions/master/api_docs/python/array_ops.html#reverse>`__

    """
    with tf.name_scope(name):
        return tf.nn.softmax(x)