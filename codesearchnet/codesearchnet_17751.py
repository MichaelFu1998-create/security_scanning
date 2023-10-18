def lower(option,value):
    '''
    Enforces lower case options and option values where appropriate
    '''
    if type(option) is str:
        option=option.lower()
    if type(value) is str:
        value=value.lower()
    return (option,value)