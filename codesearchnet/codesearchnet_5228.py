def convert_transpose(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert transpose layer.

   Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting transpose ...')
    if params['perm'][0] != 0:
        if inputs[0] in layers:
            print('!!! Cannot permute batch dimension. Result may be wrong !!!')
            layers[scope_name] = layers[inputs[0]]
        else:
            print('Skip weight matrix transpose, result may be wrong.')
    else:
        if names:
            tf_name = 'PERM' + random_string(4)
        else:
            tf_name = w_name + str(random.random())
        permute = keras.layers.Permute(params['perm'][1:], name=tf_name)
        layers[scope_name] = permute(layers[inputs[0]])