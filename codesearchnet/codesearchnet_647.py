def _to_b_h_w_n_c(self, x, x_shape):
        """(b*c, h, w, n) -> (b, h, w, n, c)"""
        x = tf.reshape(x, (-1, x_shape[4], x_shape[1], x_shape[2], x_shape[3]))
        x = tf.transpose(x, [0, 2, 3, 4, 1])
        return x