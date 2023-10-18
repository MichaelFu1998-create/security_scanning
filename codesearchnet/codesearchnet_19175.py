def closest(tokens, search_vec, limit, offset=0):
    """Return the <limit> words from <tokens> whose vectors most closely
    resemble the search_vec. Skip the first <offset> results.
    """
    return sorted(tokens,
                  key=lambda x: cosine(search_vec, word_vec(x)),
                  reverse=True)[offset:offset+limit]