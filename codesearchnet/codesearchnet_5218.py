def convert_slice(params, w_name, scope_name, inputs, layers, weights, names):
    """
    Convert slice operation.

    Args:
        params: dictionary with layer parameters
        w_name: name prefix in state_dict
        scope_name: pytorch scope name
        inputs: pytorch node inputs
        layers: dictionary with keras tensors
        weights: pytorch state_dict
        names: use short names for keras layers
    """
    print('Converting slice ...')

    if len(params['axes']) > 1:
        raise AssertionError('Cannot convert slice by multiple dimensions')

    if params['axes'][0] not in [0, 1, 2, 3]:
        raise AssertionError('Slice by dimension more than 3 or less than 0 is not supported')

    def target_layer(x, axis=int(params['axes'][0]), start=int(params['starts'][0]), end=int(params['ends'][0])):
        if axis == 0:
            return x[start:end]
        elif axis == 1:
            return x[:, start:end]
        elif axis == 2:
            return x[:, :, start:end]
        elif axis == 3:
            return x[:, :, :, start:end]

    lambda_layer = keras.layers.Lambda(target_layer)
    layers[scope_name] = lambda_layer(layers[inputs[0]])