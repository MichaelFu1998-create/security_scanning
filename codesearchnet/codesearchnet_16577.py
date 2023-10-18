def _ordinal_metric(_v1, _v2, i1, i2, n_v):
    """Metric for ordinal data."""
    if i1 > i2:
        i1, i2 = i2, i1
    return (np.sum(n_v[i1:(i2 + 1)]) - (n_v[i1] + n_v[i2]) / 2) ** 2