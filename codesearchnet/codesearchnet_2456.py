def imagenet_example(shape=(224, 224), data_format='channels_last'):
    """ Returns an example image and its imagenet class label.

    Parameters
    ----------
    shape : list of integers
        The shape of the returned image.
    data_format : str
        "channels_first" or "channels_last"

    Returns
    -------
    image : array_like
        The example image.

    label : int
        The imagenet label associated with the image.

    NOTE: This function is deprecated and will be removed in the future.
    """
    assert len(shape) == 2
    assert data_format in ['channels_first', 'channels_last']

    from PIL import Image
    path = os.path.join(os.path.dirname(__file__), 'example.png')
    image = Image.open(path)
    image = image.resize(shape)
    image = np.asarray(image, dtype=np.float32)
    image = image[:, :, :3]
    assert image.shape == shape + (3,)
    if data_format == 'channels_first':
        image = np.transpose(image, (2, 0, 1))
    return image, 282