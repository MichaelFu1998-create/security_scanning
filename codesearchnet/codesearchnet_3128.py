def make_grid(tensor, nrow=8, padding=2, pad_value=0):
    """Make a grid of images, via numpy.

    Args:
        tensor (Tensor or list): 4D mini-batch Tensor of shape (B x C x H x W)
            or a list of images all of the same size.
        nrow (int, optional): Number of images displayed in each row of the grid.
            The Final grid size is (B / nrow, nrow). Default is 8.
        padding (int, optional): amount of padding. Default is 2.
        pad_value (float, optional): Value for the padded pixels.

    """
    if not (isinstance(tensor, np.ndarray) or
            (isinstance(tensor, list) and all(isinstance(t, np.ndarray) for t in tensor))):
        raise TypeError('tensor or list of tensors expected, got {}'.format(type(tensor)))

    # if list of tensors, convert to a 4D mini-batch Tensor
    if isinstance(tensor, list):
        tensor = np.stack(tensor, 0)

    if tensor.ndim == 2:  # single image H x W
        tensor = tensor.reshape((1, tensor.shape[0], tensor.shape[1]))

    if tensor.ndim == 3:
        if tensor.shape[0] == 1:  # if single-channel, single image, convert to 3-channel
            tensor = np.concatenate((tensor, tensor, tensor), 0)
        tensor = tensor.reshape((1, tensor.shape[0], tensor.shape[1], tensor.shape[2]))

    if tensor.ndim == 4 and tensor.shape[1] == 1:  # single-channel images
        tensor = np.concatenate((tensor, tensor, tensor), 1)

    if tensor.shape[0] == 1:
        return np.squeeze(tensor)

    # make the mini-batch of images into a grid
    nmaps = tensor.shape[0]
    xmaps = min(nrow, nmaps)
    ymaps = int(math.ceil(float(nmaps) / xmaps))
    height, width = int(tensor.shape[2] + padding), int(tensor.shape[3] + padding)
    grid = np.ones((3, height * ymaps + padding, width * xmaps + padding)) * pad_value
    k = 0
    for y in range(ymaps):
        for x in range(xmaps):
            if k >= nmaps:
                break
            grid[:, y * height + padding:(y+1) * height,\
                 x * width + padding:(x+1) * width] = tensor[k]
            k = k + 1
    return grid