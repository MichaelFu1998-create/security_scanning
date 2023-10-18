def get_word_id (root):
    """
    lookup/assign a unique identify for each word root
    """
    global UNIQ_WORDS

    # in practice, this should use a microservice via some robust
    # distributed cache, e.g., Redis, Cassandra, etc.
    if root not in UNIQ_WORDS:
        UNIQ_WORDS[root] = len(UNIQ_WORDS)

    return UNIQ_WORDS[root]