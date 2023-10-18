def convert_convtranspose(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert transposed convolution layer.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting transposed convolution ...')

    if names == 'short':
        tf_name = 'C' + random_string(7)
    elif names == 'keep':
        tf_name = w_name
    else:
        tf_name = w_name + str(random.random())

    bias_name = '{0}.bias'.format(w_name)
    weights_name = '{0}.weight'.format(w_name)

    if len(weights[weights_name].numpy().shape) == 4:
        W = weights[weights_name].numpy().transpose(2, 3, 1, 0)
        height, width, n_filters, channels = W.shape

        n_groups = params['group']
        if n_groups > 1:
            raise AssertionError('Cannot convert conv1d with groups != 1')

        if params['dilations'][0] > 1:
            raise AssertionError('Cannot convert conv1d with dilation_rate != 1')

        if bias_name in weights:
            biases = weights[bias_name].numpy()
            has_bias = True
        else:
            biases = None
            has_bias = False

        input_name = inputs[0]

        if has_bias:
            weights = [W, biases]
        else:
            weights = [W]

        conv = keras.layers.Conv2DTranspose(
            filters=n_filters,
            kernel_size=(height, width),
            strides=(params['strides'][0], params['strides'][1]),
            padding='valid',
            output_padding=0,
            weights=weights,
            use_bias=has_bias,
            activation=None,
            dilation_rate=params['dilations'][0],
            bias_initializer='zeros', kernel_initializer='zeros',
            name=tf_name
        )

        layers[scope_name] = conv(layers[input_name])

        # Magic ad-hoc.
        # See the Keras issue: https://github.com/keras-team/keras/issues/6777
        layers[scope_name].set_shape(layers[scope_name]._keras_shape)

        pads = params['pads']
        if pads[0] > 0:
            assert(len(pads) == 2 or (pads[2] == pads[0] and pads[3] == pads[1]))

            crop = keras.layers.Cropping2D(
                pads[:2],
                name=tf_name + '_crop'
            )
            layers[scope_name] = crop(layers[scope_name])
    else:
        raise AssertionError('Layer is not supported for now')