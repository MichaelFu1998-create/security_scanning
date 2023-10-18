def join_phonemes(*args):
    """Joins a Hangul letter from Korean phonemes."""
    # Normalize arguments as onset, nucleus, coda.
    if len(args) == 1:
        # tuple of (onset, nucleus[, coda])
        args = args[0]
    if len(args) == 2:
        args += (CODAS[0],)
    try:
        onset, nucleus, coda = args
    except ValueError:
        raise TypeError('join_phonemes() takes at most 3 arguments')
    offset = (
        (ONSETS.index(onset) * NUM_NUCLEUSES + NUCLEUSES.index(nucleus)) *
        NUM_CODAS + CODAS.index(coda)
    )
    return unichr(FIRST_HANGUL_OFFSET + offset)