def convert_upsample_bilinear(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert upsample_bilinear2d layer.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting upsample...')

    if names == 'short':
        tf_name = 'UPSL' + random_string(4)
    elif names == 'keep':
        tf_name = w_name
    else:
        tf_name = w_name + str(random.random())

    output_size = params['output_size']
    align_corners = params['align_corners'] > 0

    def target_layer(x, size=output_size, align_corners=align_corners):
        import tensorflow as tf
        x = tf.transpose(x, [0, 2, 3, 1])
        x = tf.image.resize_images(x, size, align_corners=align_corners)
        x = tf.transpose(x, [0, 3, 1, 2])
        return x

    lambda_layer = keras.layers.Lambda(target_layer)
    layers[scope_name] = lambda_layer(layers[inputs[0]])