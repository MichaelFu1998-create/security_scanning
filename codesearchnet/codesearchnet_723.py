def fit(
        sess, network, train_op, cost, X_train, y_train, x, y_, acc=None, batch_size=100, n_epoch=100, print_freq=5,
        X_val=None, y_val=None, eval_train=True, tensorboard_dir=None, tensorboard_epoch_freq=5,
        tensorboard_weight_histograms=True, tensorboard_graph_vis=True
):
    """Training a given non time-series network by the given cost function, training data, batch_size, n_epoch etc.

    - MNIST example click `here <https://github.com/tensorlayer/tensorlayer/blob/master/example/tutorial_mnist_simple.py>`_.
    - In order to control the training details, the authors HIGHLY recommend ``tl.iterate`` see two MNIST examples `1 <https://github.com/tensorlayer/tensorlayer/blob/master/example/tutorial_mlp_dropout1.py>`_, `2 <https://github.com/tensorlayer/tensorlayer/blob/master/example/tutorial_mlp_dropout1.py>`_.

    Parameters
    ----------
    sess : Session
        TensorFlow Session.
    network : TensorLayer layer
        the network to be trained.
    train_op : TensorFlow optimizer
        The optimizer for training e.g. tf.train.AdamOptimizer.
    X_train : numpy.array
        The input of training data
    y_train : numpy.array
        The target of training data
    x : placeholder
        For inputs.
    y_ : placeholder
        For targets.
    acc : TensorFlow expression or None
        Metric for accuracy or others. If None, would not print the information.
    batch_size : int
        The batch size for training and evaluating.
    n_epoch : int
        The number of training epochs.
    print_freq : int
        Print the training information every ``print_freq`` epochs.
    X_val : numpy.array or None
        The input of validation data. If None, would not perform validation.
    y_val : numpy.array or None
        The target of validation data. If None, would not perform validation.
    eval_train : boolean
        Whether to evaluate the model during training.
        If X_val and y_val are not None, it reflects whether to evaluate the model on training data.
    tensorboard_dir : string
        path to log dir, if set, summary data will be stored to the tensorboard_dir/ directory for visualization with tensorboard. (default None)
        Also runs `tl.layers.initialize_global_variables(sess)` internally in fit() to setup the summary nodes.
    tensorboard_epoch_freq : int
        How many epochs between storing tensorboard checkpoint for visualization to log/ directory (default 5).
    tensorboard_weight_histograms : boolean
        If True updates tensorboard data in the logs/ directory for visualization
        of the weight histograms every tensorboard_epoch_freq epoch (default True).
    tensorboard_graph_vis : boolean
        If True stores the graph in the tensorboard summaries saved to log/ (default True).

    Examples
    --------
    See `tutorial_mnist_simple.py <https://github.com/tensorlayer/tensorlayer/blob/master/example/tutorial_mnist_simple.py>`_

    >>> tl.utils.fit(sess, network, train_op, cost, X_train, y_train, x, y_,
    ...            acc=acc, batch_size=500, n_epoch=200, print_freq=5,
    ...            X_val=X_val, y_val=y_val, eval_train=False)
    >>> tl.utils.fit(sess, network, train_op, cost, X_train, y_train, x, y_,
    ...            acc=acc, batch_size=500, n_epoch=200, print_freq=5,
    ...            X_val=X_val, y_val=y_val, eval_train=False,
    ...            tensorboard=True, tensorboard_weight_histograms=True, tensorboard_graph_vis=True)

    Notes
    --------
    If tensorboard_dir not None, the `global_variables_initializer` will be run inside the fit function
    in order to initialize the automatically generated summary nodes used for tensorboard visualization,
    thus `tf.global_variables_initializer().run()` before the `fit()` call will be undefined.

    """
    if X_train.shape[0] < batch_size:
        raise AssertionError("Number of training examples should be bigger than the batch size")

    if tensorboard_dir is not None:
        tl.logging.info("Setting up tensorboard ...")
        #Set up tensorboard summaries and saver
        tl.files.exists_or_mkdir(tensorboard_dir)

        #Only write summaries for more recent TensorFlow versions
        if hasattr(tf, 'summary') and hasattr(tf.summary, 'FileWriter'):
            if tensorboard_graph_vis:
                train_writer = tf.summary.FileWriter(tensorboard_dir + '/train', sess.graph)
                val_writer = tf.summary.FileWriter(tensorboard_dir + '/validation', sess.graph)
            else:
                train_writer = tf.summary.FileWriter(tensorboard_dir + '/train')
                val_writer = tf.summary.FileWriter(tensorboard_dir + '/validation')

        #Set up summary nodes
        if (tensorboard_weight_histograms):
            for param in network.all_params:
                if hasattr(tf, 'summary') and hasattr(tf.summary, 'histogram'):
                    tl.logging.info('Param name %s' % param.name)
                    tf.summary.histogram(param.name, param)

        if hasattr(tf, 'summary') and hasattr(tf.summary, 'histogram'):
            tf.summary.scalar('cost', cost)

        merged = tf.summary.merge_all()

        #Initalize all variables and summaries
        tl.layers.initialize_global_variables(sess)
        tl.logging.info("Finished! use `tensorboard --logdir=%s/` to start tensorboard" % tensorboard_dir)

    tl.logging.info("Start training the network ...")
    start_time_begin = time.time()
    tensorboard_train_index, tensorboard_val_index = 0, 0
    for epoch in range(n_epoch):
        start_time = time.time()
        loss_ep = 0
        n_step = 0
        for X_train_a, y_train_a in tl.iterate.minibatches(X_train, y_train, batch_size, shuffle=True):
            feed_dict = {x: X_train_a, y_: y_train_a}
            feed_dict.update(network.all_drop)  # enable noise layers
            loss, _ = sess.run([cost, train_op], feed_dict=feed_dict)
            loss_ep += loss
            n_step += 1
        loss_ep = loss_ep / n_step

        if tensorboard_dir is not None and hasattr(tf, 'summary'):
            if epoch + 1 == 1 or (epoch + 1) % tensorboard_epoch_freq == 0:
                for X_train_a, y_train_a in tl.iterate.minibatches(X_train, y_train, batch_size, shuffle=True):
                    dp_dict = dict_to_one(network.all_drop)  # disable noise layers
                    feed_dict = {x: X_train_a, y_: y_train_a}
                    feed_dict.update(dp_dict)
                    result = sess.run(merged, feed_dict=feed_dict)
                    train_writer.add_summary(result, tensorboard_train_index)
                    tensorboard_train_index += 1
                if (X_val is not None) and (y_val is not None):
                    for X_val_a, y_val_a in tl.iterate.minibatches(X_val, y_val, batch_size, shuffle=True):
                        dp_dict = dict_to_one(network.all_drop)  # disable noise layers
                        feed_dict = {x: X_val_a, y_: y_val_a}
                        feed_dict.update(dp_dict)
                        result = sess.run(merged, feed_dict=feed_dict)
                        val_writer.add_summary(result, tensorboard_val_index)
                        tensorboard_val_index += 1

        if epoch + 1 == 1 or (epoch + 1) % print_freq == 0:
            if (X_val is not None) and (y_val is not None):
                tl.logging.info("Epoch %d of %d took %fs" % (epoch + 1, n_epoch, time.time() - start_time))
                if eval_train is True:
                    train_loss, train_acc, n_batch = 0, 0, 0
                    for X_train_a, y_train_a in tl.iterate.minibatches(X_train, y_train, batch_size, shuffle=True):
                        dp_dict = dict_to_one(network.all_drop)  # disable noise layers
                        feed_dict = {x: X_train_a, y_: y_train_a}
                        feed_dict.update(dp_dict)
                        if acc is not None:
                            err, ac = sess.run([cost, acc], feed_dict=feed_dict)
                            train_acc += ac
                        else:
                            err = sess.run(cost, feed_dict=feed_dict)
                        train_loss += err
                        n_batch += 1
                    tl.logging.info("   train loss: %f" % (train_loss / n_batch))
                    if acc is not None:
                        tl.logging.info("   train acc: %f" % (train_acc / n_batch))
                val_loss, val_acc, n_batch = 0, 0, 0
                for X_val_a, y_val_a in tl.iterate.minibatches(X_val, y_val, batch_size, shuffle=True):
                    dp_dict = dict_to_one(network.all_drop)  # disable noise layers
                    feed_dict = {x: X_val_a, y_: y_val_a}
                    feed_dict.update(dp_dict)
                    if acc is not None:
                        err, ac = sess.run([cost, acc], feed_dict=feed_dict)
                        val_acc += ac
                    else:
                        err = sess.run(cost, feed_dict=feed_dict)
                    val_loss += err
                    n_batch += 1

                tl.logging.info("   val loss: %f" % (val_loss / n_batch))

                if acc is not None:
                    tl.logging.info("   val acc: %f" % (val_acc / n_batch))
            else:
                tl.logging.info(
                    "Epoch %d of %d took %fs, loss %f" % (epoch + 1, n_epoch, time.time() - start_time, loss_ep)
                )
    tl.logging.info("Total training time: %fs" % (time.time() - start_time_begin))