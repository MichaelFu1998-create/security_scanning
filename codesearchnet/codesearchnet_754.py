def main_restore_embedding_layer():
    """How to use Embedding layer, and how to convert IDs to vector,
    IDs to words, etc.
    """
    # Step 1: Build the embedding matrix and load the existing embedding matrix.
    vocabulary_size = 50000
    embedding_size = 128
    model_file_name = "model_word2vec_50k_128"
    batch_size = None

    print("Load existing embedding matrix and dictionaries")
    all_var = tl.files.load_npy_to_any(name=model_file_name + '.npy')
    data = all_var['data']
    count = all_var['count']
    dictionary = all_var['dictionary']
    reverse_dictionary = all_var['reverse_dictionary']

    tl.nlp.save_vocab(count, name='vocab_' + model_file_name + '.txt')

    del all_var, data, count

    load_params = tl.files.load_npz(name=model_file_name + '.npz')

    x = tf.placeholder(tf.int32, shape=[batch_size])

    emb_net = tl.layers.EmbeddingInputlayer(x, vocabulary_size, embedding_size, name='emb')

    # sess.run(tf.global_variables_initializer())
    sess.run(tf.global_variables_initializer())

    tl.files.assign_params(sess, [load_params[0]], emb_net)

    emb_net.print_params()
    emb_net.print_layers()

    # Step 2: Input word(s), output the word vector(s).
    word = b'hello'
    word_id = dictionary[word]
    print('word_id:', word_id)

    words = [b'i', b'am', b'tensor', b'layer']
    word_ids = tl.nlp.words_to_word_ids(words, dictionary, _UNK)
    context = tl.nlp.word_ids_to_words(word_ids, reverse_dictionary)
    print('word_ids:', word_ids)
    print('context:', context)

    vector = sess.run(emb_net.outputs, feed_dict={x: [word_id]})
    print('vector:', vector.shape)

    vectors = sess.run(emb_net.outputs, feed_dict={x: word_ids})
    print('vectors:', vectors.shape)