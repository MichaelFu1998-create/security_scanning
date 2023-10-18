def enumeration(*args):
    """
    Return a value check function which raises a value error if the value is not
    in a pre-defined enumeration of values.

    If you pass in a list, tuple or set as the single argument, it is assumed
    that the list/tuple/set defines the membership of the enumeration.

    If you pass in more than on argument, it is assumed the arguments themselves
    define the enumeration.

    """

    assert len(args) > 0, 'at least one argument is required'
    if len(args) == 1:
        # assume the first argument defines the membership
        members = args[0]
    else:
        # assume the arguments are the members
        members = args
    def checker(value):
        if value not in members:
            raise ValueError(value)
    return checker