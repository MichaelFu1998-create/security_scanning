def _conversion(target, source):
    '''A decorator to register namespace conversions.

    Usage
    -----
    >>> @conversion('tag_open', 'tag_.*')
    ... def tag_to_open(annotation):
    ...     annotation.namespace = 'tag_open'
    ...     return annotation
    '''

    def register(func):
        '''This decorator registers func as mapping source to target'''
        __CONVERSION__[target][source] = func
        return func

    return register