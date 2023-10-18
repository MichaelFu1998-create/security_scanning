def regenerate_good_tokens(string):
    """
    Given an input string, part of speech tags the string, then generates a list of
    ngrams that appear in the string.
    Used to define grammatically correct part of speech tag sequences.
    Returns a list of part of speech tag sequences.
    """
    toks = nltk.word_tokenize(string)
    pos_string = nltk.pos_tag(toks)
    pos_seq = [tag[1] for tag in pos_string]
    pos_ngrams = ngrams(pos_seq, 2, 4)
    sel_pos_ngrams = f7(pos_ngrams)
    return sel_pos_ngrams