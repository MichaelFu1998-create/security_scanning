def convert_reduce_sum(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert reduce_sum layer.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting reduce_sum ...')

    keepdims = params['keepdims'] > 0
    axis = params['axes']

    def target_layer(x, keepdims=keepdims, axis=axis):
        import keras.backend as K
        return K.sum(x, keepdims=keepdims, axis=axis)

    lambda_layer = keras.layers.Lambda(target_layer)
    layers[scope_name] = lambda_layer(layers[inputs[0]])