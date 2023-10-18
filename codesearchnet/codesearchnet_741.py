def build_words_dataset(words=None, vocabulary_size=50000, printable=True, unk_key='UNK'):
    """Build the words dictionary and replace rare words with 'UNK' token.
    The most common word has the smallest integer id.

    Parameters
    ----------
    words : list of str or byte
        The context in list format. You may need to do preprocessing on the words, such as lower case, remove marks etc.
    vocabulary_size : int
        The maximum vocabulary size, limiting the vocabulary size. Then the script replaces rare words with 'UNK' token.
    printable : boolean
        Whether to print the read vocabulary size of the given words.
    unk_key : str
        Represent the unknown words.

    Returns
    --------
    data : list of int
        The context in a list of ID.
    count : list of tuple and list
        Pair words and IDs.
            - count[0] is a list : the number of rare words
            - count[1:] are tuples : the number of occurrence of each word
            - e.g. [['UNK', 418391], (b'the', 1061396), (b'of', 593677), (b'and', 416629), (b'one', 411764)]
    dictionary : dictionary
        It is `word_to_id` that maps word to ID.
    reverse_dictionary : a dictionary
        It is `id_to_word` that maps ID to word.

    Examples
    --------
    >>> words = tl.files.load_matt_mahoney_text8_dataset()
    >>> vocabulary_size = 50000
    >>> data, count, dictionary, reverse_dictionary = tl.nlp.build_words_dataset(words, vocabulary_size)

    References
    -----------------
    - `tensorflow/examples/tutorials/word2vec/word2vec_basic.py <https://github.com/tensorflow/tensorflow/blob/r0.7/tensorflow/examples/tutorials/word2vec/word2vec_basic.py>`__

    """
    if words is None:
        raise Exception("words : list of str or byte")

    count = [[unk_key, -1]]
    count.extend(collections.Counter(words).most_common(vocabulary_size - 1))
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    data = list()
    unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]
        else:
            index = 0  # dictionary['UNK']
            unk_count += 1
        data.append(index)
    count[0][1] = unk_count
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    if printable:
        tl.logging.info('Real vocabulary size    %d' % len(collections.Counter(words).keys()))
        tl.logging.info('Limited vocabulary size {}'.format(vocabulary_size))
    if len(collections.Counter(words).keys()) < vocabulary_size:
        raise Exception(
            "len(collections.Counter(words).keys()) >= vocabulary_size , the limited vocabulary_size must be less than or equal to the read vocabulary_size"
        )
    return data, count, dictionary, reverse_dictionary