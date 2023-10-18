def gather(obj):
    """Retrieve objects that have been distributed, making them local again"""
    if hasattr(obj, '__distob_gather__'):
        return obj.__distob_gather__()
    elif (isinstance(obj, collections.Sequence) and 
            not isinstance(obj, string_types)):
        return [gather(subobj) for subobj in obj]
    else:
        return obj