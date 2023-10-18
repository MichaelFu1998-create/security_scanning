def process_sentence(sentence, start_word="<S>", end_word="</S>"):
    """Seperate a sentence string into a list of string words, add start_word and end_word,
    see ``create_vocab()`` and ``tutorial_tfrecord3.py``.

    Parameters
    ----------
    sentence : str
        A sentence.
    start_word : str or None
        The start word. If None, no start word will be appended.
    end_word : str or None
        The end word. If None, no end word will be appended.

    Returns
    ---------
    list of str
        A list of strings that separated into words.

    Examples
    -----------
    >>> c = "how are you?"
    >>> c = tl.nlp.process_sentence(c)
    >>> print(c)
    ['<S>', 'how', 'are', 'you', '?', '</S>']

    Notes
    -------
    - You have to install the following package.
    - `Installing NLTK <http://www.nltk.org/install.html>`__
    - `Installing NLTK data <http://www.nltk.org/data.html>`__

    """
    if start_word is not None:
        process_sentence = [start_word]
    else:
        process_sentence = []
    process_sentence.extend(nltk.tokenize.word_tokenize(sentence.lower()))

    if end_word is not None:
        process_sentence.append(end_word)
    return process_sentence