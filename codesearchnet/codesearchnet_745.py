def create_vocabulary(
        vocabulary_path, data_path, max_vocabulary_size, tokenizer=None, normalize_digits=True,
        _DIGIT_RE=re.compile(br"\d"), _START_VOCAB=None
):
    r"""Create vocabulary file (if it does not exist yet) from data file.

    Data file is assumed to contain one sentence per line. Each sentence is
    tokenized and digits are normalized (if normalize_digits is set).
    Vocabulary contains the most-frequent tokens up to max_vocabulary_size.
    We write it to vocabulary_path in a one-token-per-line format, so that later
    token in the first line gets id=0, second line gets id=1, and so on.

    Parameters
    -----------
    vocabulary_path : str
        Path where the vocabulary will be created.
    data_path : str
        Data file that will be used to create vocabulary.
    max_vocabulary_size : int
        Limit on the size of the created vocabulary.
    tokenizer : function
        A function to use to tokenize each data sentence. If None, basic_tokenizer will be used.
    normalize_digits : boolean
        If true, all digits are replaced by `0`.
    _DIGIT_RE : regular expression function
        Default is ``re.compile(br"\d")``.
    _START_VOCAB : list of str
        The pad, go, eos and unk token, default is ``[b"_PAD", b"_GO", b"_EOS", b"_UNK"]``.

    References
    ----------
    - Code from ``/tensorflow/models/rnn/translation/data_utils.py``

    """
    if _START_VOCAB is None:
        _START_VOCAB = [b"_PAD", b"_GO", b"_EOS", b"_UNK"]
    if not gfile.Exists(vocabulary_path):
        tl.logging.info("Creating vocabulary %s from data %s" % (vocabulary_path, data_path))
        vocab = {}
        with gfile.GFile(data_path, mode="rb") as f:
            counter = 0
            for line in f:
                counter += 1
                if counter % 100000 == 0:
                    tl.logging.info("  processing line %d" % counter)
                tokens = tokenizer(line) if tokenizer else basic_tokenizer(line)
                for w in tokens:
                    word = re.sub(_DIGIT_RE, b"0", w) if normalize_digits else w
                    if word in vocab:
                        vocab[word] += 1
                    else:
                        vocab[word] = 1
            vocab_list = _START_VOCAB + sorted(vocab, key=vocab.get, reverse=True)
            if len(vocab_list) > max_vocabulary_size:
                vocab_list = vocab_list[:max_vocabulary_size]
            with gfile.GFile(vocabulary_path, mode="wb") as vocab_file:
                for w in vocab_list:
                    vocab_file.write(w + b"\n")
    else:
        tl.logging.info("Vocabulary %s from data %s exists" % (vocabulary_path, data_path))