def initialize_vocabulary(vocabulary_path):
    """Initialize vocabulary from file, return the `word_to_id` (dictionary)
    and `id_to_word` (list).

    We assume the vocabulary is stored one-item-per-line, so a file will result in a vocabulary {"dog": 0, "cat": 1}, and this function will also return the reversed-vocabulary ["dog", "cat"].

    Parameters
    -----------
    vocabulary_path : str
        Path to the file containing the vocabulary.

    Returns
    --------
    vocab : dictionary
        a dictionary that maps word to ID.
    rev_vocab : list of int
        a list that maps ID to word.

    Examples
    ---------
    >>> Assume 'test' contains
    dog
    cat
    bird
    >>> vocab, rev_vocab = tl.nlp.initialize_vocabulary("test")
    >>> print(vocab)
    >>> {b'cat': 1, b'dog': 0, b'bird': 2}
    >>> print(rev_vocab)
    >>> [b'dog', b'cat', b'bird']

    Raises
    -------
    ValueError : if the provided vocabulary_path does not exist.

    """
    if gfile.Exists(vocabulary_path):
        rev_vocab = []
        with gfile.GFile(vocabulary_path, mode="rb") as f:
            rev_vocab.extend(f.readlines())
        rev_vocab = [tf.compat.as_bytes(line.strip()) for line in rev_vocab]
        vocab = dict([(x, y) for (y, x) in enumerate(rev_vocab)])
        return vocab, rev_vocab
    else:
        raise ValueError("Vocabulary file %s not found.", vocabulary_path)