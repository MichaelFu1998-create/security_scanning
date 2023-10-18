def convert_concat(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert concatenation.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting concat ...')
    concat_nodes = [layers[i] for i in inputs]

    if len(concat_nodes) == 1:
        # no-op
        layers[scope_name] = concat_nodes[0]
        return

    if names == 'short':
        tf_name = 'CAT' + random_string(5)
    elif names == 'keep':
        tf_name = w_name
    else:
        tf_name = w_name + str(random.random())

    cat = keras.layers.Concatenate(name=tf_name, axis=params['axis'])
    layers[scope_name] = cat(concat_nodes)