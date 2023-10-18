def from_keras(cls, model, bounds, input_shape=None,
                   channel_axis=3, preprocessing=(0, 1)):
        """Alternative constructor for a TensorFlowModel that
        accepts a `tf.keras.Model` instance.

        Parameters
        ----------
        model : `tensorflow.keras.Model`
            A `tensorflow.keras.Model` that accepts a single input tensor
            and returns a single output tensor representing logits.
        bounds : tuple
            Tuple of lower and upper bound for the pixel values, usually
            (0, 1) or (0, 255).
        input_shape : tuple
            The shape of a single input, e.g. (28, 28, 1) for MNIST.
            If None, tries to get the the shape from the model's
            input_shape attribute.
        channel_axis : int
            The index of the axis that represents color channels.
        preprocessing: 2-element tuple with floats or numpy arrays
            Elementwises preprocessing of input; we first subtract the first
            element of preprocessing from the input and then divide the input
            by the second element.

        """
        import tensorflow as tf
        if input_shape is None:
            try:
                input_shape = model.input_shape[1:]
            except AttributeError:
                raise ValueError(
                    'Please specify input_shape manually or '
                    'provide a model with an input_shape attribute')
        with tf.keras.backend.get_session().as_default():
            inputs = tf.placeholder(tf.float32, (None,) + input_shape)
            logits = model(inputs)
            return cls(inputs, logits, bounds=bounds,
                       channel_axis=channel_axis, preprocessing=preprocessing)