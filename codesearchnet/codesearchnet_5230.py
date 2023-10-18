def convert_squeeze(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert squeeze operation.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting squeeze ...')

    if len(params['axes']) > 1:
        raise AssertionError('Cannot convert squeeze by multiple dimensions')

    def target_layer(x, axis=int(params['axes'][0])):
        import tensorflow as tf
        return tf.squeeze(x, axis=axis)

    lambda_layer = keras.layers.Lambda(target_layer)
    layers[scope_name] = lambda_layer(layers[inputs[0]])