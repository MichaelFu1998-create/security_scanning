def build_reverse_dictionary(word_to_id):
    """Given a dictionary that maps word to integer id.
    Returns a reverse dictionary that maps a id to word.

    Parameters
    ----------
    word_to_id : dictionary
        that maps word to ID.

    Returns
    --------
    dictionary
        A dictionary that maps IDs to words.

    """
    reverse_dictionary = dict(zip(word_to_id.values(), word_to_id.keys()))
    return reverse_dictionary