def cmp_features(feat1, feat2):
    """Compare features.

    This returns a number in the range [0, 1] representing a comparison of two
    feature bundles.

    If one of the bundles is negative, -1 is returned (for unknown values)

    If the bundles are identical, 1 is returned.

    If they are inverses of one another, 0 is returned.

    Otherwise, a float representing their similarity is returned.

    Parameters
    ----------
    feat1 : int
        A feature bundle
    feat2 : int
        A feature bundle

    Returns
    -------
    float
        A comparison of the feature bundles

    Examples
    --------
    >>> cmp_features(ipa_to_features('l')[0], ipa_to_features('l')[0])
    1.0
    >>> cmp_features(ipa_to_features('l')[0], ipa_to_features('n')[0])
    0.8709677419354839
    >>> cmp_features(ipa_to_features('l')[0], ipa_to_features('z')[0])
    0.8709677419354839
    >>> cmp_features(ipa_to_features('l')[0], ipa_to_features('i')[0])
    0.564516129032258

    """
    if feat1 < 0 or feat2 < 0:
        return -1.0
    if feat1 == feat2:
        return 1.0

    magnitude = len(_FEATURE_MASK)
    featxor = feat1 ^ feat2
    diffbits = 0
    # print(featxor)
    while featxor:
        if featxor & 0b1:
            diffbits += 1
        featxor >>= 1
    # print(diffbits)
    return 1 - (diffbits / (2 * magnitude))