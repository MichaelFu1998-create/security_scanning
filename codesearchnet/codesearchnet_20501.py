def get_dict_leaves(data):
    """
    Given a nested dictionary, this returns all its leave elements in a list.

    :param adict:

    :return: list
    """
    result = []
    if isinstance(data, dict):
        for item in data.values():
            result.extend(get_dict_leaves(item))
    elif isinstance(data, list):
        result.extend(data)
    else:
        result.append(data)

    return result