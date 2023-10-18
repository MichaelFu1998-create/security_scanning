def convert_flatten(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert reshape(view).

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting flatten ...')

    if names == 'short':
        tf_name = 'R' + random_string(7)
    elif names == 'keep':
        tf_name = w_name
    else:
        tf_name = w_name + str(random.random())

    reshape = keras.layers.Reshape([-1], name=tf_name)
    layers[scope_name] = reshape(layers[inputs[0]])