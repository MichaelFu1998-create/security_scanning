def basic_tokenizer(sentence, _WORD_SPLIT=re.compile(b"([.,!?\"':;)(])")):
    """Very basic tokenizer: split the sentence into a list of tokens.

    Parameters
    -----------
    sentence : tensorflow.python.platform.gfile.GFile Object
    _WORD_SPLIT : regular expression for word spliting.


    Examples
    --------
    >>> see create_vocabulary
    >>> from tensorflow.python.platform import gfile
    >>> train_path = "wmt/giga-fren.release2"
    >>> with gfile.GFile(train_path + ".en", mode="rb") as f:
    >>>    for line in f:
    >>>       tokens = tl.nlp.basic_tokenizer(line)
    >>>       tl.logging.info(tokens)
    >>>       exit()
    [b'Changing', b'Lives', b'|', b'Changing', b'Society', b'|', b'How',
      b'It', b'Works', b'|', b'Technology', b'Drives', b'Change', b'Home',
      b'|', b'Concepts', b'|', b'Teachers', b'|', b'Search', b'|', b'Overview',
      b'|', b'Credits', b'|', b'HHCC', b'Web', b'|', b'Reference', b'|',
      b'Feedback', b'Virtual', b'Museum', b'of', b'Canada', b'Home', b'Page']

    References
    ----------
    - Code from ``/tensorflow/models/rnn/translation/data_utils.py``

    """
    words = []
    sentence = tf.compat.as_bytes(sentence)
    for space_separated_fragment in sentence.strip().split():
        words.extend(re.split(_WORD_SPLIT, space_separated_fragment))
    return [w for w in words if w]