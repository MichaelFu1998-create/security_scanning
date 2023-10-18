def _engine_affinity(obj):
    """Which engine or engines are preferred for processing this object
    Returns: (location, weight)
      location (integer or tuple): engine id (or in the case of a distributed
      array a tuple (engine_id_list, distaxis)).
      weight(integer): Proportional to the cost of moving the object to a
        different engine. Currently just taken to be the size of data.
    """
    from distob import engine
    this_engine = engine.eid
    if isinstance(obj, numbers.Number) or obj is None:
        return (this_engine, 0)
    elif hasattr(obj, '__engine_affinity__'):
        # This case includes Remote subclasses and DistArray
        return obj.__engine_affinity__
    else:
        return (this_engine, _rough_size(obj))