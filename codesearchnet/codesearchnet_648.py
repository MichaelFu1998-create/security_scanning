def _tf_repeat(self, a, repeats):
        """Tensorflow version of np.repeat for 1D"""
        # https://github.com/tensorflow/tensorflow/issues/8521

        if len(a.get_shape()) != 1:
            raise AssertionError("This is not a 1D Tensor")

        a = tf.expand_dims(a, -1)
        a = tf.tile(a, [1, repeats])
        a = self.tf_flatten(a)
        return a