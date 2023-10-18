def cosine_similarity(v1, v2):
    """Cosine similarity [-1, 1].

    Parameters
    ----------
    v1, v2 : Tensor
        Tensor with the same shape [batch_size, n_feature].

    References
    ----------
    - `Wiki <https://en.wikipedia.org/wiki/Cosine_similarity>`__.

    """

    return tf.reduce_sum(tf.multiply(v1, v2), 1) / \
        (tf.sqrt(tf.reduce_sum(tf.multiply(v1, v1), 1)) *
         tf.sqrt(tf.reduce_sum(tf.multiply(v2, v2), 1)))