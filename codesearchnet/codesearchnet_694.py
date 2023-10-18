def distort_image(image, thread_id):
    """Perform random distortions on an image.
    Args:
        image: A float32 Tensor of shape [height, width, 3] with values in [0, 1).
        thread_id: Preprocessing thread id used to select the ordering of color
        distortions. There should be a multiple of 2 preprocessing threads.
    Returns:````
        distorted_image: A float32 Tensor of shape [height, width, 3] with values in
        [0, 1].
    """
    # Randomly flip horizontally.
    with tf.name_scope("flip_horizontal"):  # , values=[image]): # DH MOdify
        # with tf.name_scope("flip_horizontal", values=[image]):
        image = tf.image.random_flip_left_right(image)
    # Randomly distort the colors based on thread id.
    color_ordering = thread_id % 2
    with tf.name_scope("distort_color"):  # , values=[image]): # DH MOdify
        # with tf.name_scope("distort_color", values=[image]): # DH MOdify
        if color_ordering == 0:
            image = tf.image.random_brightness(image, max_delta=32. / 255.)
            image = tf.image.random_saturation(image, lower=0.5, upper=1.5)
            image = tf.image.random_hue(image, max_delta=0.032)
            image = tf.image.random_contrast(image, lower=0.5, upper=1.5)
        elif color_ordering == 1:
            image = tf.image.random_brightness(image, max_delta=32. / 255.)
            image = tf.image.random_contrast(image, lower=0.5, upper=1.5)
            image = tf.image.random_saturation(image, lower=0.5, upper=1.5)
            image = tf.image.random_hue(image, max_delta=0.032)
        # The random_* ops do not necessarily clamp.
        image = tf.clip_by_value(image, 0.0, 1.0)

    return image