def _get_detail_value(var, attr):
    """
    Given a variable and one of its attributes that are available inside of
    a template, return its 'method' if it is a callable, its class name if it
    is a model manager, otherwise return its value
    """
    value = getattr(var, attr)
    # Rename common Django class names
    kls = getattr(getattr(value, '__class__', ''), '__name__', '')
    if kls in ('ManyRelatedManager', 'RelatedManager', 'EmptyManager'):
        return kls
    if callable(value):
        return 'routine'
    return value