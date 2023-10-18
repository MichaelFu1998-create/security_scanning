def convert_elementwise_add(
    params, w_name, scope_name, inputs, layers, weights, names
):
    """
    Convert elementwise addition.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting elementwise_add ...')
    if 'broadcast' in params:
        model0 = layers[inputs[0]]
        model1 = layers[inputs[1]]

        if names == 'short':
            tf_name = 'A' + random_string(7)
        elif names == 'keep':
            tf_name = w_name
        else:
            tf_name = w_name + str(random.random())

        def target_layer(x):
            layer = tf.add(x[0], x[1])
            return layer

        lambda_layer = keras.layers.Lambda(target_layer, name=tf_name)
        layers[scope_name] = lambda_layer([layers[inputs[0]], layers[inputs[1]]])
    else:
        model0 = layers[inputs[0]]
        model1 = layers[inputs[1]]

        if names == 'short':
            tf_name = 'A' + random_string(7)
        elif names == 'keep':
            tf_name = w_name
        else:
            tf_name = w_name + str(random.random())

        add = keras.layers.Add(name=tf_name)
        layers[scope_name] = add([model0, model1])