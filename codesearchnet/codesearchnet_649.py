def _tf_batch_map_coordinates(self, inputs, coords):
        """Batch version of tf_map_coordinates

        Only supports 2D feature maps

        Parameters
        ----------
        inputs : ``tf.Tensor``
            shape = (b*c, h, w)
        coords : ``tf.Tensor``
            shape = (b*c, h, w, n, 2)

        Returns
        -------
        ``tf.Tensor``
            A Tensor with the shape as (b*c, h, w, n)

        """
        input_shape = inputs.get_shape()
        coords_shape = coords.get_shape()
        batch_channel = tf.shape(inputs)[0]
        input_h = int(input_shape[1])
        input_w = int(input_shape[2])
        kernel_n = int(coords_shape[3])
        n_coords = input_h * input_w * kernel_n

        coords_lt = tf.cast(tf.floor(coords), 'int32')
        coords_rb = tf.cast(tf.ceil(coords), 'int32')
        coords_lb = tf.stack([coords_lt[:, :, :, :, 0], coords_rb[:, :, :, :, 1]], axis=-1)
        coords_rt = tf.stack([coords_rb[:, :, :, :, 0], coords_lt[:, :, :, :, 1]], axis=-1)

        idx = self._tf_repeat(tf.range(batch_channel), n_coords)

        vals_lt = self._get_vals_by_coords(inputs, coords_lt, idx, (batch_channel, input_h, input_w, kernel_n))
        vals_rb = self._get_vals_by_coords(inputs, coords_rb, idx, (batch_channel, input_h, input_w, kernel_n))
        vals_lb = self._get_vals_by_coords(inputs, coords_lb, idx, (batch_channel, input_h, input_w, kernel_n))
        vals_rt = self._get_vals_by_coords(inputs, coords_rt, idx, (batch_channel, input_h, input_w, kernel_n))

        coords_offset_lt = coords - tf.cast(coords_lt, 'float32')

        vals_t = vals_lt + (vals_rt - vals_lt) * coords_offset_lt[:, :, :, :, 0]
        vals_b = vals_lb + (vals_rb - vals_lb) * coords_offset_lt[:, :, :, :, 0]
        mapped_vals = vals_t + (vals_b - vals_t) * coords_offset_lt[:, :, :, :, 1]

        return mapped_vals