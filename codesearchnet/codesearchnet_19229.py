def autohide(obj):
    """
    Automatically hide setup() and teardown() methods, recursively.
    """
    # Members on obj
    for name, item in six.iteritems(vars(obj)):
        if callable(item) and name in ('setup', 'teardown'):
            item = hide(item)
    # Recurse into class members
    for name, subclass in class_members(obj):
        autohide(subclass)