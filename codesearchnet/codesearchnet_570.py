def adjust_hue(im, hout=0.66, is_offset=True, is_clip=True, is_random=False):
    """Adjust hue of an RGB image.

    This is a convenience method that converts an RGB image to float representation, converts it to HSV, add an offset to the hue channel, converts back to RGB and then back to the original data type.
    For TF, see `tf.image.adjust_hue <https://www.tensorflow.org/api_docs/python/tf/image/adjust_hue>`__.and `tf.image.random_hue <https://www.tensorflow.org/api_docs/python/tf/image/random_hue>`__.

    Parameters
    -----------
    im : numpy.array
        An image with values between 0 and 255.
    hout : float
        The scale value for adjusting hue.
            - If is_offset is False, set all hue values to this value. 0 is red; 0.33 is green; 0.66 is blue.
            - If is_offset is True, add this value as the offset to the hue channel.
    is_offset : boolean
        Whether `hout` is added on HSV as offset or not. Default is True.
    is_clip : boolean
        If HSV value smaller than 0, set to 0. Default is True.
    is_random : boolean
        If True, randomly change hue. Default is False.

    Returns
    -------
    numpy.array
        A processed image.

    Examples
    ---------
    Random, add a random value between -0.2 and 0.2 as the offset to every hue values.

    >>> im_hue = tl.prepro.adjust_hue(image, hout=0.2, is_offset=True, is_random=False)

    Non-random, make all hue to green.

    >>> im_green = tl.prepro.adjust_hue(image, hout=0.66, is_offset=False, is_random=False)

    References
    -----------
    - `tf.image.random_hue <https://www.tensorflow.org/api_docs/python/tf/image/random_hue>`__.
    - `tf.image.adjust_hue <https://www.tensorflow.org/api_docs/python/tf/image/adjust_hue>`__.
    - `StackOverflow: Changing image hue with python PIL <https://stackoverflow.com/questions/7274221/changing-image-hue-with-python-pil>`__.

    """
    hsv = rgb_to_hsv(im)
    if is_random:
        hout = np.random.uniform(-hout, hout)

    if is_offset:
        hsv[..., 0] += hout
    else:
        hsv[..., 0] = hout

    if is_clip:
        hsv[..., 0] = np.clip(hsv[..., 0], 0, np.inf)  # Hao : can remove green dots

    rgb = hsv_to_rgb(hsv)
    return rgb