def retrieve_seq_length_op3(data, pad_val=0):  # HangSheng: return tensor for sequence length, if input is tf.string
    """Return tensor for sequence length, if input is ``tf.string``."""
    data_shape_size = data.get_shape().ndims
    if data_shape_size == 3:
        return tf.reduce_sum(tf.cast(tf.reduce_any(tf.not_equal(data, pad_val), axis=2), dtype=tf.int32), 1)
    elif data_shape_size == 2:
        return tf.reduce_sum(tf.cast(tf.not_equal(data, pad_val), dtype=tf.int32), 1)
    elif data_shape_size == 1:
        raise ValueError("retrieve_seq_length_op3: data has wrong shape!")
    else:
        raise ValueError(
            "retrieve_seq_length_op3: handling data_shape_size %s hasn't been implemented!" % (data_shape_size)
        )