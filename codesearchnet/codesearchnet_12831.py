def _resolveambig(subseq):
    """ 
    Randomly resolves iupac hetero codes. This is a shortcut
    for now, we could instead use the phased alleles in RAD loci.
    """
    N = []
    for col in subseq:
        rand = np.random.binomial(1, 0.5)
        N.append([_AMBIGS[i][rand] for i in col])
    return np.array(N)