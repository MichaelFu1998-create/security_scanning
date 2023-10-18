def convert_maxpool3(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert 3d Max pooling.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """

    print('Converting pooling ...')

    if names == 'short':
        tf_name = 'P' + random_string(7)
    elif names == 'keep':
        tf_name = w_name
    else:
        tf_name = w_name + str(random.random())

    if 'kernel_shape' in params:
        height, width, depth = params['kernel_shape']
    else:
        height, width, depth = params['kernel_size']

    if 'strides' in params:
        stride_height, stride_width, stride_depth = params['strides']
    else:
        stride_height, stride_width, stride_depth = params['stride']

    if 'pads' in params:
        padding_h, padding_w, padding_d, _, _ = params['pads']
    else:
        padding_h, padding_w, padding_d = params['padding']

    input_name = inputs[0]
    if padding_h > 0 and padding_w > 0 and padding_d > 0:
        padding_name = tf_name + '_pad'
        padding_layer = keras.layers.ZeroPadding3D(
            padding=(padding_h, padding_w, padding_d),
            name=padding_name
        )
        layers[padding_name] = padding_layer(layers[inputs[0]])
        input_name = padding_name

    # Pooling type
    pooling = keras.layers.MaxPooling3D(
        pool_size=(height, width, depth),
        strides=(stride_height, stride_width, stride_depth),
        padding='valid',
        name=tf_name
    )

    layers[scope_name] = pooling(layers[input_name])