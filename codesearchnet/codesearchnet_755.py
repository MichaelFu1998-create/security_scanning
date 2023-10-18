def main_lstm_generate_text():
    """Generate text by Synced sequence input and output."""
    # rnn model and update  (describtion: see tutorial_ptb_lstm.py)
    init_scale = 0.1
    learning_rate = 1.0
    max_grad_norm = 5
    sequence_length = 20
    hidden_size = 200
    max_epoch = 4
    max_max_epoch = 100
    lr_decay = 0.9
    batch_size = 20

    top_k_list = [1, 3, 5, 10]
    print_length = 30

    model_file_name = "model_generate_text.npz"

    # ===== Prepare Data
    words = customized_read_words(input_fpath="data/trump/trump_text.txt")

    vocab = tl.nlp.create_vocab([words], word_counts_output_file='vocab.txt', min_word_count=1)
    vocab = tl.nlp.Vocabulary('vocab.txt', unk_word="<UNK>")
    vocab_size = vocab.unk_id + 1
    train_data = [vocab.word_to_id(word) for word in words]

    # Set the seed to generate sentence.
    seed = "it is a"
    # seed = basic_clean_str(seed).split()
    seed = nltk.tokenize.word_tokenize(seed)
    print('seed : %s' % seed)

    sess = tf.InteractiveSession()

    # ===== Define model
    input_data = tf.placeholder(tf.int32, [batch_size, sequence_length])
    targets = tf.placeholder(tf.int32, [batch_size, sequence_length])
    # Testing (Evaluation), for generate text
    input_data_test = tf.placeholder(tf.int32, [1, 1])

    def inference(x, is_train, sequence_length, reuse=None):
        """If reuse is True, the inferences use the existing parameters,
        then different inferences share the same parameters.
        """
        print("\nsequence_length: %d, is_train: %s, reuse: %s" % (sequence_length, is_train, reuse))
        rnn_init = tf.random_uniform_initializer(-init_scale, init_scale)
        with tf.variable_scope("model", reuse=reuse):
            network = EmbeddingInputlayer(x, vocab_size, hidden_size, rnn_init, name='embedding')
            network = RNNLayer(
                network, cell_fn=tf.contrib.rnn.BasicLSTMCell, cell_init_args={
                    'forget_bias': 0.0,
                    'state_is_tuple': True
                }, n_hidden=hidden_size, initializer=rnn_init, n_steps=sequence_length, return_last=False,
                return_seq_2d=True, name='lstm1'
            )
            lstm1 = network
            network = DenseLayer(network, vocab_size, W_init=rnn_init, b_init=rnn_init, act=None, name='output')
        return network, lstm1

    # Inference for Training
    network, lstm1 = inference(input_data, is_train=True, sequence_length=sequence_length, reuse=None)
    # Inference for generate text, sequence_length=1
    network_test, lstm1_test = inference(input_data_test, is_train=False, sequence_length=1, reuse=True)
    y_linear = network_test.outputs
    y_soft = tf.nn.softmax(y_linear)

    # y_id = tf.argmax(tf.nn.softmax(y), 1)

    # ===== Define train ops
    def loss_fn(outputs, targets, batch_size, sequence_length):
        # Returns the cost function of Cross-entropy of two sequences, implement
        # softmax internally.
        # outputs : 2D tensor [n_examples, n_outputs]
        # targets : 2D tensor [n_examples, n_outputs]
        # n_examples = batch_size * sequence_length
        # so
        # cost is the averaged cost of each mini-batch (concurrent process).
        loss = tf.contrib.legacy_seq2seq.sequence_loss_by_example(
            [outputs], [tf.reshape(targets, [-1])], [tf.ones([batch_size * sequence_length])]
        )
        cost = tf.reduce_sum(loss) / batch_size
        return cost

    # Cost for Training
    cost = loss_fn(network.outputs, targets, batch_size, sequence_length)

    # Truncated Backpropagation for training
    with tf.variable_scope('learning_rate'):
        lr = tf.Variable(0.0, trainable=False)
    # You can get all trainable parameters as follow.
    # tvars = tf.trainable_variables()
    # Alternatively, you can specify the parameters for training as follw.
    #  tvars = network.all_params      $ all parameters
    #  tvars = network.all_params[1:]  $ parameters except embedding matrix
    # Train the whole network.
    tvars = network.all_params
    grads, _ = tf.clip_by_global_norm(tf.gradients(cost, tvars), max_grad_norm)
    optimizer = tf.train.GradientDescentOptimizer(lr)
    train_op = optimizer.apply_gradients(zip(grads, tvars))

    # ===== Training
    sess.run(tf.global_variables_initializer())

    print("\nStart learning a model to generate text")
    for i in range(max_max_epoch):
        # decrease the learning_rate after ``max_epoch``, by multipling lr_decay.
        new_lr_decay = lr_decay**max(i - max_epoch, 0.0)
        sess.run(tf.assign(lr, learning_rate * new_lr_decay))

        print("Epoch: %d/%d Learning rate: %.8f" % (i + 1, max_max_epoch, sess.run(lr)))
        epoch_size = ((len(train_data) // batch_size) - 1) // sequence_length

        start_time = time.time()
        costs = 0.0
        iters = 0
        # reset all states at the begining of every epoch
        state1 = tl.layers.initialize_rnn_state(lstm1.initial_state)
        for step, (x, y) in enumerate(tl.iterate.ptb_iterator(train_data, batch_size, sequence_length)):
            _cost, state1, _ = sess.run(
                [cost, lstm1.final_state, train_op], feed_dict={
                    input_data: x,
                    targets: y,
                    lstm1.initial_state: state1
                }
            )
            costs += _cost
            iters += sequence_length

            if step % (epoch_size // 10) == 1:
                print(
                    "%.3f perplexity: %.3f speed: %.0f wps" %
                    (step * 1.0 / epoch_size, np.exp(costs / iters), iters * batch_size / (time.time() - start_time))
                )
        train_perplexity = np.exp(costs / iters)
        # print("Epoch: %d Train Perplexity: %.3f" % (i + 1, train_perplexity))
        print("Epoch: %d/%d Train Perplexity: %.3f" % (i + 1, max_max_epoch, train_perplexity))

        # for diversity in diversity_list:
        # testing: sample from top k words
        for top_k in top_k_list:
            # Testing, generate some text from a given seed.
            state1 = tl.layers.initialize_rnn_state(lstm1_test.initial_state)
            # state2 = tl.layers.initialize_rnn_state(lstm2_test.initial_state)
            outs_id = [vocab.word_to_id(w) for w in seed]
            # feed the seed to initialize the state for generation.
            for ids in outs_id[:-1]:
                a_id = np.asarray(ids).reshape(1, 1)
                state1 = sess.run(
                    [lstm1_test.final_state], feed_dict={
                        input_data_test: a_id,
                        lstm1_test.initial_state: state1
                    }
                )
            # feed the last word in seed, and start to generate sentence.
            a_id = outs_id[-1]
            for _ in range(print_length):
                a_id = np.asarray(a_id).reshape(1, 1)
                out, state1 = sess.run(
                    [y_soft, lstm1_test.final_state], feed_dict={
                        input_data_test: a_id,
                        lstm1_test.initial_state: state1
                    }
                )
                # Without sampling
                # a_id = np.argmax(out[0])
                # Sample from all words, if vocab_size is large,
                # this may have numeric error.
                # a_id = tl.nlp.sample(out[0], diversity)
                # Sample from the top k words.
                a_id = tl.nlp.sample_top(out[0], top_k=top_k)
                outs_id.append(a_id)
            sentence = [vocab.id_to_word(w) for w in outs_id]
            sentence = " ".join(sentence)
            # print(diversity, ':', sentence)
            print(top_k, ':', sentence)

    print("Save model")
    tl.files.save_npz(network_test.all_params, name=model_file_name)