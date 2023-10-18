def _mergeDictionaries(*args):
    ''' merge dictionaries of dictionaries recursively, with elements from
        dictionaries earlier in the argument sequence taking precedence
    '''
    # to support merging of OrderedDicts, copy the result type from the first
    # argument:
    result = type(args[0])()
    for k, v in itertools.chain(*[x.items() for x in args]):
        if not k in result:
            result[k] = v
        elif isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _mergeDictionaries(result[k], v)
    return result