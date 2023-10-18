def get_feature(vector, feature):
    """Get a feature vector.

    This returns a list of ints, equal in length to the vector input,
        representing presence/absence/neutrality with respect to a particular
        phonetic feature.

    Parameters
    ----------
    vector : list
        A tuple or list of ints representing the phonetic features of a phone
        or series of phones (such as is returned by the ipa_to_features
        function)
    feature : str
        A feature name from the set:

            - ``consonantal``
            - ``sonorant``
            - ``syllabic``
            - ``labial``
            - ``round``
            - ``coronal``
            - ``anterior``
            - ``distributed``
            - ``dorsal``
            - ``high``
            - ``low``
            - ``back``
            - ``tense``
            - ``pharyngeal``
            - ``ATR``
            - ``voice``
            - ``spread_glottis``
            - ``constricted_glottis``
            - ``continuant``
            - ``strident``
            - ``lateral``
            - ``delayed_release``
            - ``nasal``

    Returns
    -------
    list of ints
        A list indicating presence/absence/neutrality with respect to the
        feature

    Raises
    ------
    AttributeError
        feature must be one of ...

    Examples
    --------
    >>> tails = ipa_to_features('telz')
    >>> get_feature(tails, 'consonantal')
    [1, -1, 1, 1]
    >>> get_feature(tails, 'sonorant')
    [-1, 1, 1, -1]
    >>> get_feature(tails, 'nasal')
    [-1, -1, -1, -1]
    >>> get_feature(tails, 'coronal')
    [1, -1, 1, 1]

    """
    # :param bool binary: if False, -1, 0, & 1 represent -, 0, & +
    #           if True, only binary oppositions are allowed:
    #           0 & 1 represent - & + and 0s are mapped to -

    if feature not in _FEATURE_MASK:
        raise AttributeError(
            "feature must be one of: '"
            + "', '".join(
                (
                    'consonantal',
                    'sonorant',
                    'syllabic',
                    'labial',
                    'round',
                    'coronal',
                    'anterior',
                    'distributed',
                    'dorsal',
                    'high',
                    'low',
                    'back',
                    'tense',
                    'pharyngeal',
                    'ATR',
                    'voice',
                    'spread_glottis',
                    'constricted_glottis',
                    'continuant',
                    'strident',
                    'lateral',
                    'delayed_release',
                    'nasal',
                )
            )
            + "'"
        )

    # each feature mask contains two bits, one each for - and +
    mask = _FEATURE_MASK[feature]
    # the lower bit represents +
    pos_mask = mask >> 1
    retvec = []
    for char in vector:
        if char < 0:
            retvec.append(float('NaN'))
        else:
            masked = char & mask
            if masked == 0:
                retvec.append(0)  # 0
            elif masked == mask:
                retvec.append(2)  # +/-
            elif masked & pos_mask:
                retvec.append(1)  # +
            else:
                retvec.append(-1)  # -

    return retvec