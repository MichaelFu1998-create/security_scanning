def dict_to_label(dict):
    '''
    Transform a dict with keys `label`, `type` and `language` into a
    :class:`Label`.

    Only the `label` key is mandatory. If `type` is not present, it will
    default to `prefLabel`. If `language` is not present, it will default
    to `und`.

    If the argument passed is not a dict, this method just
    returns the argument.
    '''
    try:
        return Label(
            dict['label'],
            dict.get('type', 'prefLabel'),
            dict.get('language', 'und')
        )
    except (KeyError, AttributeError, TypeError):
        return dict