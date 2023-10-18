def sentence_to_token_ids(
        sentence, vocabulary, tokenizer=None, normalize_digits=True, UNK_ID=3, _DIGIT_RE=re.compile(br"\d")
):
    """Convert a string to list of integers representing token-ids.

    For example, a sentence "I have a dog" may become tokenized into
    ["I", "have", "a", "dog"] and with vocabulary {"I": 1, "have": 2,
    "a": 4, "dog": 7"} this function will return [1, 2, 4, 7].

    Parameters
    -----------
    sentence : tensorflow.python.platform.gfile.GFile Object
        The sentence in bytes format to convert to token-ids, see ``basic_tokenizer()`` and ``data_to_token_ids()``.
    vocabulary : dictionary
        Mmapping tokens to integers.
    tokenizer : function
        A function to use to tokenize each sentence. If None, ``basic_tokenizer`` will be used.
    normalize_digits : boolean
        If true, all digits are replaced by 0.

    Returns
    --------
    list of int
        The token-ids for the sentence.

    """
    if tokenizer:
        words = tokenizer(sentence)
    else:
        words = basic_tokenizer(sentence)
    if not normalize_digits:
        return [vocabulary.get(w, UNK_ID) for w in words]
    # Normalize digits by 0 before looking words up in the vocabulary.
    return [vocabulary.get(re.sub(_DIGIT_RE, b"0", w), UNK_ID) for w in words]