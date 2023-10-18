def merge_list(list1, list2, identifiers=None):
    """
    Merges ``list2`` on top of ``list1``.

    If both lists contain dictionaries which have keys specified
    in ``identifiers`` which have equal values, those dicts will
    be merged (dicts in ``list2`` will override dicts in ``list1``).
    The remaining elements will be summed in order to create a list
    which contains elements of both lists.

    :param list1: ``list`` from template
    :param list2: ``list`` from config
    :param identifiers: ``list`` or ``None``
    :returns: merged ``list``
    """
    identifiers = identifiers or []
    dict_map = {'list1': OrderedDict(), 'list2': OrderedDict()}
    counter = 1
    for list_ in [list1, list2]:
        container = dict_map['list{0}'.format(counter)]
        for el in list_:
            # merge by internal python id by default
            key = id(el)
            # if el is a dict, merge by keys specified in ``identifiers``
            if isinstance(el, dict):
                for id_key in identifiers:
                    if id_key in el:
                        key = el[id_key]
                        break
            container[key] = deepcopy(el)
        counter += 1
    merged = merge_config(dict_map['list1'], dict_map['list2'])
    return list(merged.values())