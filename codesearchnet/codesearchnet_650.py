def _tf_batch_map_offsets(self, inputs, offsets, grid_offset):
        """Batch map offsets into input

        Parameters
        ------------
        inputs : ``tf.Tensor``
            shape = (b, h, w, c)
        offsets: ``tf.Tensor``
            shape = (b, h, w, 2*n)
        grid_offset: `tf.Tensor``
            Offset grids shape = (h, w, n, 2)

        Returns
        -------
        ``tf.Tensor``
            A Tensor with the shape as (b, h, w, c)

        """
        input_shape = inputs.get_shape()
        batch_size = tf.shape(inputs)[0]
        kernel_n = int(int(offsets.get_shape()[3]) / 2)
        input_h = input_shape[1]
        input_w = input_shape[2]
        channel = input_shape[3]

        # inputs (b, h, w, c) --> (b*c, h, w)
        inputs = self._to_bc_h_w(inputs, input_shape)

        # offsets (b, h, w, 2*n) --> (b, h, w, n, 2)
        offsets = tf.reshape(offsets, (batch_size, input_h, input_w, kernel_n, 2))
        # offsets (b, h, w, n, 2) --> (b*c, h, w, n, 2)
        # offsets = tf.tile(offsets, [channel, 1, 1, 1, 1])

        coords = tf.expand_dims(grid_offset, 0)  # grid_offset --> (1, h, w, n, 2)
        coords = tf.tile(coords, [batch_size, 1, 1, 1, 1]) + offsets  # grid_offset --> (b, h, w, n, 2)

        # clip out of bound
        coords = tf.stack(
            [
                tf.clip_by_value(coords[:, :, :, :, 0], 0.0, tf.cast(input_h - 1, 'float32')),
                tf.clip_by_value(coords[:, :, :, :, 1], 0.0, tf.cast(input_w - 1, 'float32'))
            ], axis=-1
        )
        coords = tf.tile(coords, [channel, 1, 1, 1, 1])

        mapped_vals = self._tf_batch_map_coordinates(inputs, coords)
        # (b*c, h, w, n) --> (b, h, w, n, c)
        mapped_vals = self._to_b_h_w_n_c(mapped_vals, [batch_size, input_h, input_w, kernel_n, channel])

        return mapped_vals