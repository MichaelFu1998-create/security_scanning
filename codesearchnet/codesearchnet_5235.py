def convert_adaptive_max_pool2d(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert convert_adaptive_max_pool2d layer.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting adaptive_avg_pool2d...')

    if names == 'short':
        tf_name = 'APOL' + random_string(4)
    elif names == 'keep':
        tf_name = w_name
    else:
        tf_name = w_name + str(random.random())

    global_pool = keras.layers.GlobalMaxPooling2D(data_format='channels_first', name=tf_name)
    layers[scope_name] = global_pool(layers[inputs[0]])

    def target_layer(x):
        import keras
        return keras.backend.expand_dims(x)

    lambda_layer = keras.layers.Lambda(target_layer, name=tf_name + 'E')
    layers[scope_name] = lambda_layer(layers[scope_name])  # double expand dims
    layers[scope_name] = lambda_layer(layers[scope_name])