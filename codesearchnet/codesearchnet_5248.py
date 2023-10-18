def convert_upsample(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert nearest upsampling layer.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting upsample...')

    if params['mode'] != 'nearest':
        raise AssertionError('Cannot convert non-nearest upsampling')

    if names == 'short':
        tf_name = 'UPSL' + random_string(4)
    elif names == 'keep':
        tf_name = w_name
    else:
        tf_name = w_name + str(random.random())

    if 'height_scale' in params:
        scale = (params['height_scale'], params['width_scale'])
    elif len(inputs) == 2:
        scale = layers[inputs[-1] + '_np'][-2:]

    upsampling = keras.layers.UpSampling2D(
        size=scale, name=tf_name
    )
    layers[scope_name] = upsampling(layers[inputs[0]])