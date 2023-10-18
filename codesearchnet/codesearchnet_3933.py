def map_vals(func, dict_):
    """
    applies a function to each of the keys in a dictionary

    Args:
        func (callable): a function or indexable object
        dict_ (dict): a dictionary

    Returns:
        newdict: transformed dictionary

    CommandLine:
        python -m ubelt.util_dict map_vals

    Example:
        >>> import ubelt as ub
        >>> dict_ = {'a': [1, 2, 3], 'b': []}
        >>> func = len
        >>> newdict = ub.map_vals(func, dict_)
        >>> assert newdict ==  {'a': 3, 'b': 0}
        >>> print(newdict)
        >>> # Can also use indexables as `func`
        >>> dict_ = {'a': 0, 'b': 1}
        >>> func = [42, 21]
        >>> newdict = ub.map_vals(func, dict_)
        >>> assert newdict ==  {'a': 42, 'b': 21}
        >>> print(newdict)
    """
    if not hasattr(func, '__call__'):
        func = func.__getitem__
    keyval_list = [(key, func(val)) for key, val in six.iteritems(dict_)]
    dictclass = OrderedDict if isinstance(dict_, OrderedDict) else dict
    newdict = dictclass(keyval_list)
    # newdict = type(dict_)(keyval_list)
    return newdict