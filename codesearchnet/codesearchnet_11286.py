def ipa_to_features(ipa):
    """Convert IPA to features.

    This translates an IPA string of one or more phones to a list of ints
    representing the features of the string.

    Parameters
    ----------
    ipa : str
        The IPA representation of a phone or series of phones

    Returns
    -------
    list of ints
        A representation of the features of the input string

    Examples
    --------
    >>> ipa_to_features('mut')
    [2709662981243185770, 1825831513894594986, 2783230754502126250]
    >>> ipa_to_features('fon')
    [2781702983095331242, 1825831531074464170, 2711173160463936106]
    >>> ipa_to_features('telz')
    [2783230754502126250, 1826957430176000426, 2693158761954453926,
    2783230754501863834]

    """
    features = []
    pos = 0
    ipa = normalize('NFD', text_type(ipa.lower()))

    maxsymlen = max(len(_) for _ in _PHONETIC_FEATURES)

    while pos < len(ipa):
        found_match = False
        for i in range(maxsymlen, 0, -1):
            if (
                pos + i - 1 <= len(ipa)
                and ipa[pos : pos + i] in _PHONETIC_FEATURES
            ):
                features.append(_PHONETIC_FEATURES[ipa[pos : pos + i]])
                pos += i
                found_match = True

        if not found_match:
            features.append(-1)
            pos += 1

    return features