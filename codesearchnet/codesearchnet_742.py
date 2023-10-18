def words_to_word_ids(data=None, word_to_id=None, unk_key='UNK'):
    """Convert a list of string (words) to IDs.

    Parameters
    ----------
    data : list of string or byte
        The context in list format
    word_to_id : a dictionary
        that maps word to ID.
    unk_key : str
        Represent the unknown words.

    Returns
    --------
    list of int
        A list of IDs to represent the context.

    Examples
    --------
    >>> words = tl.files.load_matt_mahoney_text8_dataset()
    >>> vocabulary_size = 50000
    >>> data, count, dictionary, reverse_dictionary = tl.nlp.build_words_dataset(words, vocabulary_size, True)
    >>> context = [b'hello', b'how', b'are', b'you']
    >>> ids = tl.nlp.words_to_word_ids(words, dictionary)
    >>> context = tl.nlp.word_ids_to_words(ids, reverse_dictionary)
    >>> print(ids)
    [6434, 311, 26, 207]
    >>> print(context)
    [b'hello', b'how', b'are', b'you']

    References
    ---------------
    - `tensorflow.models.rnn.ptb.reader <https://github.com/tensorflow/tensorflow/tree/master/tensorflow/models/rnn/ptb>`__

    """
    if data is None:
        raise Exception("data : list of string or byte")
    if word_to_id is None:
        raise Exception("word_to_id : a dictionary")
    # if isinstance(data[0], six.string_types):
    #     tl.logging.info(type(data[0]))
    #     # exit()
    #     tl.logging.info(data[0])
    #     tl.logging.info(word_to_id)
    #     return [word_to_id[str(word)] for word in data]
    # else:

    word_ids = []
    for word in data:
        if word_to_id.get(word) is not None:
            word_ids.append(word_to_id[word])
        else:
            word_ids.append(word_to_id[unk_key])
    return word_ids