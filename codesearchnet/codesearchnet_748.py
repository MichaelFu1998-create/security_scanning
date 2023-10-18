def data_to_token_ids(
        data_path, target_path, vocabulary_path, tokenizer=None, normalize_digits=True, UNK_ID=3,
        _DIGIT_RE=re.compile(br"\d")
):
    """Tokenize data file and turn into token-ids using given vocabulary file.

    This function loads data line-by-line from data_path, calls the above
    sentence_to_token_ids, and saves the result to target_path. See comment
    for sentence_to_token_ids on the details of token-ids format.

    Parameters
    -----------
    data_path : str
        Path to the data file in one-sentence-per-line format.
    target_path : str
        Path where the file with token-ids will be created.
    vocabulary_path : str
        Path to the vocabulary file.
    tokenizer : function
        A function to use to tokenize each sentence. If None, ``basic_tokenizer`` will be used.
    normalize_digits : boolean
        If true, all digits are replaced by 0.

    References
    ----------
    - Code from ``/tensorflow/models/rnn/translation/data_utils.py``

    """
    if not gfile.Exists(target_path):
        tl.logging.info("Tokenizing data in %s" % data_path)
        vocab, _ = initialize_vocabulary(vocabulary_path)
        with gfile.GFile(data_path, mode="rb") as data_file:
            with gfile.GFile(target_path, mode="w") as tokens_file:
                counter = 0
                for line in data_file:
                    counter += 1
                    if counter % 100000 == 0:
                        tl.logging.info("  tokenizing line %d" % counter)
                    token_ids = sentence_to_token_ids(
                        line, vocab, tokenizer, normalize_digits, UNK_ID=UNK_ID, _DIGIT_RE=_DIGIT_RE
                    )
                    tokens_file.write(" ".join([str(tok) for tok in token_ids]) + "\n")
    else:
        tl.logging.info("Target path %s exists" % target_path)