def count_dict_values(dict_of_counters: Mapping[X, Sized]) -> typing.Counter[X]:
    """Count the number of elements in each value (can be list, Counter, etc).

    :param dict_of_counters: A dictionary of things whose lengths can be measured (lists, Counters, dicts)
    :return: A Counter with the same keys as the input but the count of the length of the values list/tuple/set/Counter
    """
    return Counter({
        k: len(v)
        for k, v in dict_of_counters.items()
    })