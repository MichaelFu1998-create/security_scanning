def get_object(name: str):
    """Get a modelx object from its full name."""
    # TODO: Duplicate of system.get_object
    elms = name.split(".")
    parent = get_models()[elms.pop(0)]
    while len(elms) > 0:
        obj = elms.pop(0)
        parent = getattr(parent, obj)

    return parent