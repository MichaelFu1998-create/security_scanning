def dict_to_note(dict):
    '''
    Transform a dict with keys `note`, `type` and `language` into a
    :class:`Note`.

    Only the `note` key is mandatory. If `type` is not present, it will
    default to `note`. If `language` is not present, it will default to `und`.
    If `markup` is not present it will default to `None`.

    If the argument passed is already a :class:`Note`, this method just returns
    the argument.
    '''
    if isinstance(dict, Note):
        return dict
    return Note(
        dict['note'],
        dict.get('type', 'note'),
        dict.get('language', 'und'),
        dict.get('markup')
    )