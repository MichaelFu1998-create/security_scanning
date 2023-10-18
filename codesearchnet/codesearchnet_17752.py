def to_float(option,value):
    '''
    Converts string values to floats when appropriate
    '''
    if type(value) is str:
        try:
            value=float(value)
        except ValueError:
            pass
    return (option,value)