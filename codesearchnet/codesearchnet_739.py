def read_analogies_file(eval_file='questions-words.txt', word2id=None):
    """Reads through an analogy question file, return its id format.

    Parameters
    ----------
    eval_file : str
        The file name.
    word2id : dictionary
        a dictionary that maps word to ID.

    Returns
    --------
    numpy.array
        A ``[n_examples, 4]`` numpy array containing the analogy question's word IDs.

    Examples
    ---------
    The file should be in this format

    >>> : capital-common-countries
    >>> Athens Greece Baghdad Iraq
    >>> Athens Greece Bangkok Thailand
    >>> Athens Greece Beijing China
    >>> Athens Greece Berlin Germany
    >>> Athens Greece Bern Switzerland
    >>> Athens Greece Cairo Egypt
    >>> Athens Greece Canberra Australia
    >>> Athens Greece Hanoi Vietnam
    >>> Athens Greece Havana Cuba

    Get the tokenized analogy question data

    >>> words = tl.files.load_matt_mahoney_text8_dataset()
    >>> data, count, dictionary, reverse_dictionary = tl.nlp.build_words_dataset(words, vocabulary_size, True)
    >>> analogy_questions = tl.nlp.read_analogies_file(eval_file='questions-words.txt', word2id=dictionary)
    >>> print(analogy_questions)
    [[ 3068  1248  7161  1581]
    [ 3068  1248 28683  5642]
    [ 3068  1248  3878   486]
    ...,
    [ 1216  4309 19982 25506]
    [ 1216  4309  3194  8650]
    [ 1216  4309   140   312]]

    """
    if word2id is None:
        word2id = {}

    questions = []
    questions_skipped = 0
    with open(eval_file, "rb") as analogy_f:
        for line in analogy_f:
            if line.startswith(b":"):  # Skip comments.
                continue
            words = line.strip().lower().split(b" ")  # lowercase
            ids = [word2id.get(w.strip()) for w in words]
            if None in ids or len(ids) != 4:
                questions_skipped += 1
            else:
                questions.append(np.array(ids))
    tl.logging.info("Eval analogy file: %s" % eval_file)
    tl.logging.info("Questions: %d", len(questions))
    tl.logging.info("Skipped: %d", questions_skipped)
    analogy_questions = np.array(questions, dtype=np.int32)
    return analogy_questions