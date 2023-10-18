def batch_transformer(U, thetas, out_size, name='BatchSpatialTransformer2dAffine'):
    """Batch Spatial Transformer function for `2D Affine Transformation <https://en.wikipedia.org/wiki/Affine_transformation>`__.

    Parameters
    ----------
    U : list of float
        tensor of inputs [batch, height, width, num_channels]
    thetas : list of float
        a set of transformations for each input [batch, num_transforms, 6]
    out_size : list of int
        the size of the output [out_height, out_width]
    name : str
        optional function name

    Returns
    ------
    float
        Tensor of size [batch * num_transforms, out_height, out_width, num_channels]

    """
    with tf.variable_scope(name):
        num_batch, num_transforms = map(int, thetas.get_shape().as_list()[:2])
        indices = [[i] * num_transforms for i in xrange(num_batch)]
        input_repeated = tf.gather(U, tf.reshape(indices, [-1]))
        return transformer(input_repeated, thetas, out_size)