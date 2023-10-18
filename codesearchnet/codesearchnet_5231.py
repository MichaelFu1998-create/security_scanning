def convert_unsqueeze(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert unsqueeze operation.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting unsqueeze ...')

    if names == 'short':
        tf_name = 'UNSQ' + random_string(4)
    elif names == 'keep':
        tf_name = w_name
    else:
        tf_name = w_name + str(random.random())

    def target_layer(x):
        import keras
        return keras.backend.expand_dims(x)

    lambda_layer = keras.layers.Lambda(target_layer, name=tf_name + 'E')
    layers[scope_name] = lambda_layer(layers[inputs[0]])