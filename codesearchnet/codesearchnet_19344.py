def weighted_replicate(seq, weights, n):
    """Return n selections from seq, with the count of each element of
    seq proportional to the corresponding weight (filling in fractions
    randomly).
    >>> weighted_replicate('ABC', [1,2,1], 4)
    ['A', 'B', 'B', 'C']"""
    assert len(seq) == len(weights)
    weights = normalize(weights)
    wholes = [int(w*n) for w in weights]
    fractions = [(w*n) % 1 for w in weights]
    return (flatten([x] * nx for x, nx in zip(seq, wholes))
            + weighted_sample_with_replacement(seq, fractions, n - sum(wholes)))