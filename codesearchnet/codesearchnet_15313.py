def dict_to_source(dict):
    '''
    Transform a dict with key 'citation' into a :class:`Source`.

    If the argument passed is already a :class:`Source`, this method just
    returns the argument.
    '''

    if isinstance(dict, Source):
        return dict
    return Source(
        dict['citation'],
        dict.get('markup')
    )