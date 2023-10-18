def check_visitors(cls):
    """Check that a checker's visitors are correctly named.

    A checker has methods named visit_NODETYPE, but it's easy to mis-name
    a visit method, and it will never be called.  This decorator checks
    the class to see that all of its visitors are named after an existing
    node class.
    """
    for name in dir(cls):
        if name.startswith("visit_"):
            if name[6:] not in CLASS_NAMES:
                raise Exception(u"Method {} doesn't correspond to a node class".format(name))
    return cls