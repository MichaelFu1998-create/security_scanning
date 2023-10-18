def get_matches(word, tokens, limit, offset=0):
    """Return words from <tokens> that are most closely related to <word>."""
    return closest(tokens, word_vec(word), limit, offset)