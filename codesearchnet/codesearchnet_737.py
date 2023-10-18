def create_vocab(sentences, word_counts_output_file, min_word_count=1):
    """Creates the vocabulary of word to word_id.

    See ``tutorial_tfrecord3.py``.

    The vocabulary is saved to disk in a text file of word counts. The id of each
    word in the file is its corresponding 0-based line number.

    Parameters
    ------------
    sentences : list of list of str
        All sentences for creating the vocabulary.
    word_counts_output_file : str
        The file name.
    min_word_count : int
        Minimum number of occurrences for a word.

    Returns
    --------
    :class:`SimpleVocabulary`
        The simple vocabulary object, see :class:`Vocabulary` for more.

    Examples
    --------
    Pre-process sentences

    >>> captions = ["one two , three", "four five five"]
    >>> processed_capts = []
    >>> for c in captions:
    >>>     c = tl.nlp.process_sentence(c, start_word="<S>", end_word="</S>")
    >>>     processed_capts.append(c)
    >>> print(processed_capts)
    ...[['<S>', 'one', 'two', ',', 'three', '</S>'], ['<S>', 'four', 'five', 'five', '</S>']]

    Create vocabulary

    >>> tl.nlp.create_vocab(processed_capts, word_counts_output_file='vocab.txt', min_word_count=1)
    Creating vocabulary.
      Total words: 8
      Words in vocabulary: 8
      Wrote vocabulary file: vocab.txt

    Get vocabulary object

    >>> vocab = tl.nlp.Vocabulary('vocab.txt', start_word="<S>", end_word="</S>", unk_word="<UNK>")
    INFO:tensorflow:Initializing vocabulary from file: vocab.txt
    [TL] Vocabulary from vocab.txt : <S> </S> <UNK>
    vocabulary with 10 words (includes start_word, end_word, unk_word)
        start_id: 2
        end_id: 3
        unk_id: 9
        pad_id: 0

    """
    tl.logging.info("Creating vocabulary.")

    counter = Counter()

    for c in sentences:
        counter.update(c)
        # tl.logging.info('c',c)
    tl.logging.info("    Total words: %d" % len(counter))

    # Filter uncommon words and sort by descending count.
    word_counts = [x for x in counter.items() if x[1] >= min_word_count]
    word_counts.sort(key=lambda x: x[1], reverse=True)
    word_counts = [("<PAD>", 0)] + word_counts  # 1st id should be reserved for padding
    # tl.logging.info(word_counts)
    tl.logging.info("    Words in vocabulary: %d" % len(word_counts))

    # Write out the word counts file.
    with tf.gfile.FastGFile(word_counts_output_file, "w") as f:
        f.write("\n".join(["%s %d" % (w, c) for w, c in word_counts]))
    tl.logging.info("    Wrote vocabulary file: %s" % word_counts_output_file)

    # Create the vocabulary dictionary.
    reverse_vocab = [x[0] for x in word_counts]
    unk_id = len(reverse_vocab)
    vocab_dict = dict([(x, y) for (y, x) in enumerate(reverse_vocab)])
    vocab = SimpleVocabulary(vocab_dict, unk_id)

    return vocab