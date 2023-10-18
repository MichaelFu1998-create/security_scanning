def cross_entropy_reward_loss(logits, actions, rewards, name=None):
    """Calculate the loss for Policy Gradient Network.

    Parameters
    ----------
    logits : tensor
        The network outputs without softmax. This function implements softmax inside.
    actions : tensor or placeholder
        The agent actions.
    rewards : tensor or placeholder
        The rewards.

    Returns
    --------
    Tensor
        The TensorFlow loss function.

    Examples
    ----------
    >>> states_batch_pl = tf.placeholder(tf.float32, shape=[None, D])
    >>> network = InputLayer(states_batch_pl, name='input')
    >>> network = DenseLayer(network, n_units=H, act=tf.nn.relu, name='relu1')
    >>> network = DenseLayer(network, n_units=3, name='out')
    >>> probs = network.outputs
    >>> sampling_prob = tf.nn.softmax(probs)
    >>> actions_batch_pl = tf.placeholder(tf.int32, shape=[None])
    >>> discount_rewards_batch_pl = tf.placeholder(tf.float32, shape=[None])
    >>> loss = tl.rein.cross_entropy_reward_loss(probs, actions_batch_pl, discount_rewards_batch_pl)
    >>> train_op = tf.train.RMSPropOptimizer(learning_rate, decay_rate).minimize(loss)

    """
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=actions, logits=logits, name=name)

    return tf.reduce_sum(tf.multiply(cross_entropy, rewards))