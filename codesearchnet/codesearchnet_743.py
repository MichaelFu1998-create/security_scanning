def save_vocab(count=None, name='vocab.txt'):
    """Save the vocabulary to a file so the model can be reloaded.

    Parameters
    ----------
    count : a list of tuple and list
        count[0] is a list : the number of rare words,
        count[1:] are tuples : the number of occurrence of each word,
        e.g. [['UNK', 418391], (b'the', 1061396), (b'of', 593677), (b'and', 416629), (b'one', 411764)]

    Examples
    ---------
    >>> words = tl.files.load_matt_mahoney_text8_dataset()
    >>> vocabulary_size = 50000
    >>> data, count, dictionary, reverse_dictionary = tl.nlp.build_words_dataset(words, vocabulary_size, True)
    >>> tl.nlp.save_vocab(count, name='vocab_text8.txt')
    >>> vocab_text8.txt
    UNK 418391
    the 1061396
    of 593677
    and 416629
    one 411764
    in 372201
    a 325873
    to 316376

    """
    if count is None:
        count = []

    pwd = os.getcwd()
    vocabulary_size = len(count)
    with open(os.path.join(pwd, name), "w") as f:
        for i in xrange(vocabulary_size):
            f.write("%s %d\n" % (tf.compat.as_text(count[i][0]), count[i][1]))
    tl.logging.info("%d vocab saved to %s in %s" % (vocabulary_size, name, pwd))