def _modify(item, func):
    """
    Modifies each item.keys() string based on the func passed in.
    Often used with inflection's camelize or underscore methods.

    :param item: dictionary representing item to be modified
    :param func: function to run on each key string
    :return: dictionary where each key has been modified by func.
    """
    result = dict()
    for key in item:
        result[func(key)] = item[key]
    return result