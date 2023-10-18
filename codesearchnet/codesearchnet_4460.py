def can_sequence(obj):
    """Can the elements of a sequence."""
    if istype(obj, sequence_types):
        t = type(obj)
        return t([can(i) for i in obj])
    else:
        return obj