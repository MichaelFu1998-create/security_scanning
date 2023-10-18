def convert_reshape(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert reshape layer.

   Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting reshape ...')
    if names == 'short':
        tf_name = 'RESH' + random_string(4)
    elif names == 'keep':
        tf_name = w_name
    else:
        tf_name = w_name + str(random.random())

    if len(inputs) > 1:
        if layers[inputs[1]][0] == -1:
            print('Cannot deduct batch size! It will be omitted, but result may be wrong.')

        reshape = keras.layers.Reshape(layers[inputs[1] + '_np'], name=tf_name)
        layers[scope_name] = reshape(layers[inputs[0]])
    else:
        if inputs[0] in layers:
            reshape = keras.layers.Reshape(params['shape'][1:], name=tf_name)
            layers[scope_name] = reshape(layers[inputs[0]])
        else:
            print('Skip weight matrix transpose, but result may be wrong.')