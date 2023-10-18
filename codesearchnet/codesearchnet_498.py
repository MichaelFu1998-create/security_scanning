def atrous_conv1d(
        prev_layer,
        n_filter=32,
        filter_size=2,
        stride=1,
        dilation=1,
        act=None,
        padding='SAME',
        data_format='NWC',
        W_init=tf.truncated_normal_initializer(stddev=0.02),
        b_init=tf.constant_initializer(value=0.0),
        W_init_args=None,
        b_init_args=None,
        name='atrous_1d',
):
    """Simplified version of :class:`AtrousConv1dLayer`.

    Parameters
    ----------
    prev_layer : :class:`Layer`
        Previous layer.
    n_filter : int
        The number of filters.
    filter_size : int
        The filter size.
    stride : tuple of int
        The strides: (height, width).
    dilation : int
        The filter dilation size.
    act : activation function
        The activation function of this layer.
    padding : str
        The padding algorithm type: "SAME" or "VALID".
    data_format : str
        Default is 'NWC' as it is a 1D CNN.
    W_init : initializer
        The initializer for the weight matrix.
    b_init : initializer or None
        The initializer for the bias vector. If None, skip biases.
    W_init_args : dictionary
        The arguments for the weight matrix initializer.
    b_init_args : dictionary
        The arguments for the bias vector initializer.
    name : str
        A unique layer name.

    Returns
    -------
    :class:`Layer`
        A :class:`AtrousConv1dLayer` object

    """
    return Conv1dLayer(
        prev_layer=prev_layer,
        act=act,
        shape=(filter_size, int(prev_layer.outputs.get_shape()[-1]), n_filter),
        stride=stride,
        padding=padding,
        dilation_rate=dilation,
        data_format=data_format,
        W_init=W_init,
        b_init=b_init,
        W_init_args=W_init_args,
        b_init_args=b_init_args,
        name=name,
    )