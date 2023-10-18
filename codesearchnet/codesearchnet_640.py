def advanced_indexing_op(inputs, index):
    """Advanced Indexing for Sequences, returns the outputs by given sequence lengths.
    When return the last output :class:`DynamicRNNLayer` uses it to get the last outputs with the sequence lengths.

    Parameters
    -----------
    inputs : tensor for data
        With shape of [batch_size, n_step(max), n_features]
    index : tensor for indexing
        Sequence length in Dynamic RNN. [batch_size]

    Examples
    ---------
    >>> import numpy as np
    >>> import tensorflow as tf
    >>> import tensorlayer as tl
    >>> batch_size, max_length, n_features = 3, 5, 2
    >>> z = np.random.uniform(low=-1, high=1, size=[batch_size, max_length, n_features]).astype(np.float32)
    >>> b_z = tf.constant(z)
    >>> sl = tf.placeholder(dtype=tf.int32, shape=[batch_size])
    >>> o = advanced_indexing_op(b_z, sl)
    >>>
    >>> sess = tf.InteractiveSession()
    >>> tl.layers.initialize_global_variables(sess)
    >>>
    >>> order = np.asarray([1,1,2])
    >>> print("real",z[0][order[0]-1], z[1][order[1]-1], z[2][order[2]-1])
    >>> y = sess.run([o], feed_dict={sl:order})
    >>> print("given",order)
    >>> print("out", y)
    real [-0.93021595  0.53820813] [-0.92548317 -0.77135968] [ 0.89952248  0.19149846]
    given [1 1 2]
    out [array([[-0.93021595,  0.53820813],
                [-0.92548317, -0.77135968],
                [ 0.89952248,  0.19149846]], dtype=float32)]

    References
    -----------
    - Modified from TFlearn (the original code is used for fixed length rnn), `references <https://github.com/tflearn/tflearn/blob/master/tflearn/layers/recurrent.py>`__.

    """
    batch_size = tf.shape(inputs)[0]
    # max_length = int(inputs.get_shape()[1])    # for fixed length rnn, length is given
    max_length = tf.shape(inputs)[1]  # for dynamic_rnn, length is unknown
    dim_size = int(inputs.get_shape()[2])
    index = tf.range(0, batch_size) * max_length + (index - 1)
    flat = tf.reshape(inputs, [-1, dim_size])
    relevant = tf.gather(flat, index)
    return relevant