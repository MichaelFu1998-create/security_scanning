def _count_PIS(seqsamp, N):
    """ filters for loci with >= N PIS """
    counts = [Counter(col) for col in seqsamp.T if not ("-" in col or "N" in col)]
    pis = [i.most_common(2)[1][1] > 1 for i in counts if len(i.most_common(2))>1]
    if sum(pis) >= N:
        return sum(pis)
    else:
        return 0