def convert_avgpool(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert Average pooling.

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
        height, width = params['kernel_shape']
    else:
        height, width = params['kernel_size']

    if 'strides' in params:
        stride_height, stride_width = params['strides']
    else:
        stride_height, stride_width = params['stride']

    if 'pads' in params:
        padding_h, padding_w, _, _ = params['pads']
    else:
        padding_h, padding_w = params['padding']

    input_name = inputs[0]
    pad = 'valid' 

    if height % 2 == 1 and width % 2 == 1 and \
       height // 2 == padding_h and width // 2 == padding_w and \
       stride_height == 1 and stride_width == 1:
        pad = 'same'
    else:
        padding_name = tf_name + '_pad'
        padding_layer = keras.layers.ZeroPadding2D(
            padding=(padding_h, padding_w),
            name=padding_name
        )
        layers[padding_name] = padding_layer(layers[inputs[0]])
        input_name = padding_name

    # Pooling type AveragePooling2D
    pooling = keras.layers.AveragePooling2D(
        pool_size=(height, width),
        strides=(stride_height, stride_width),
        padding=pad,
        name=tf_name,
        data_format='channels_first'
    )

    layers[scope_name] = pooling(layers[input_name])