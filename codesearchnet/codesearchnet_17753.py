def to_bool(option,value):
    '''
    Converts string values to booleans when appropriate
    '''
    if type(value) is str:
        if value.lower() == 'true':
            value=True
        elif value.lower() == 'false':
            value=False
    return (option,value)