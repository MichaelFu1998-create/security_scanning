def _mirrorStructure(dictionary, value):
    ''' create a new nested dictionary object with the same structure as
        'dictionary', but with all scalar values replaced with 'value'
    '''
    result = type(dictionary)()
    for k in dictionary.keys():
        if isinstance(dictionary[k], dict):
            result[k] = _mirrorStructure(dictionary[k], value)
        else:
            result[k] = value
    return result