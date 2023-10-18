def zero_state(self, batch_size, dtype=LayersConfig.tf_dtype):
        """Return zero-filled state tensor(s).
        Args:
          batch_size: int, float, or unit Tensor representing the batch size.
        Returns:
          tensor of shape '[batch_size x shape[0] x shape[1] x num_features]
          filled with zeros

        """
        shape = self.shape
        num_features = self.num_features
        # TODO : TypeError: 'NoneType' object is not subscriptable
        zeros = tf.zeros([batch_size, shape[0], shape[1], num_features * 2], dtype=dtype)
        return zeros