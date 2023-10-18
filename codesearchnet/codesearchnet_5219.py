def convert_clip(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert clip operation.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting clip ...')

    if params['min'] == 0:
        print("using ReLU({0})".format(params['max']))
        layer = keras.layers.ReLU(max_value=params['max'])
    else:
        def target_layer(x, vmin=params['min'], vmax=params['max']):
            import tensorflow as tf
            return tf.clip_by_value(x, vmin, vmax)
        layer = keras.layers.Lambda(target_layer)

    layers[scope_name] = layer(layers[inputs[0]])