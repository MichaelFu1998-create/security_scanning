def predict(sess, network, X, x, y_op, batch_size=None):
    """
    Return the predict results of given non time-series network.

    Parameters
    ----------
    sess : Session
        TensorFlow Session.
    network : TensorLayer layer
        The network.
    X : numpy.array
        The inputs.
    x : placeholder
        For inputs.
    y_op : placeholder
        The argmax expression of softmax outputs.
    batch_size : int or None
        The batch size for prediction, when dataset is large, we should use minibatche for prediction;
        if dataset is small, we can set it to None.

    Examples
    --------
    See `tutorial_mnist_simple.py <https://github.com/tensorlayer/tensorlayer/blob/master/example/tutorial_mnist_simple.py>`_

    >>> y = network.outputs
    >>> y_op = tf.argmax(tf.nn.softmax(y), 1)
    >>> print(tl.utils.predict(sess, network, X_test, x, y_op))

    """
    if batch_size is None:
        dp_dict = dict_to_one(network.all_drop)  # disable noise layers
        feed_dict = {
            x: X,
        }
        feed_dict.update(dp_dict)
        return sess.run(y_op, feed_dict=feed_dict)
    else:
        result = None
        for X_a, _ in tl.iterate.minibatches(X, X, batch_size, shuffle=False):
            dp_dict = dict_to_one(network.all_drop)
            feed_dict = {
                x: X_a,
            }
            feed_dict.update(dp_dict)
            result_a = sess.run(y_op, feed_dict=feed_dict)
            if result is None:
                result = result_a
            else:
                result = np.concatenate((result, result_a))
        if result is None:
            if len(X) % batch_size != 0:
                dp_dict = dict_to_one(network.all_drop)
                feed_dict = {
                    x: X[-(len(X) % batch_size):, :],
                }
                feed_dict.update(dp_dict)
                result_a = sess.run(y_op, feed_dict=feed_dict)
                result = result_a
        else:
            if len(X) != len(result) and len(X) % batch_size != 0:
                dp_dict = dict_to_one(network.all_drop)
                feed_dict = {
                    x: X[-(len(X) % batch_size):, :],
                }
                feed_dict.update(dp_dict)
                result_a = sess.run(y_op, feed_dict=feed_dict)
                result = np.concatenate((result, result_a))
        return result