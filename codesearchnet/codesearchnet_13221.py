def serialize_obj(obj):
    '''Custom serialization functionality for working with advanced data types.

    - numpy arrays are converted to lists
    - lists are recursively serialized element-wise

    '''

    if isinstance(obj, np.integer):
        return int(obj)

    elif isinstance(obj, np.floating):
        return float(obj)

    elif isinstance(obj, np.ndarray):
        return obj.tolist()

    elif isinstance(obj, list):
        return [serialize_obj(x) for x in obj]

    elif isinstance(obj, Observation):
        return {k: serialize_obj(v) for k, v in six.iteritems(obj._asdict())}

    return obj