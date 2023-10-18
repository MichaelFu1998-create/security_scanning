def convert_shape(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert shape operation.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting shape ...')

    def target_layer(x):
        import tensorflow as tf
        return tf.shape(x)

    lambda_layer = keras.layers.Lambda(target_layer)
    layers[scope_name] = lambda_layer(layers[inputs[0]])