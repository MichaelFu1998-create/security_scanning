def _check_stop_list(stop):
    """
    Check stop words list
    ref: https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/feature_extraction/text.py#L87-L95
    """
    if stop == "thai":
        return THAI_STOP_WORDS
    elif isinstance(stop, six.string_types):
        raise ValueError("not a built-in stop list: %s" % stop)
    elif stop is None:
        return None
    # assume it's a collection
    return frozenset(stop)