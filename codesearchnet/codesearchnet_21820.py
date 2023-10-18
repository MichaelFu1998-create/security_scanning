def _ufunc_move_input(obj, location, bshape):
    """Copy ufunc input `obj` to new engine location(s) unless obj is scalar.

    If the input is requested to be distributed to multiple engines, this
    function will also take care of broadcasting along the distributed axis.

    If the input obj is a scalar, it will be passed through unchanged.

    Args:
      obj (array_like or scalar): one of the inputs to a ufunc
      location (integer or tuple): If an integer, this specifies a single
        engine id to which an array input should be moved. If it is a tuple,
        location[0] is a list of engine ids for distributing the array input
        and location[1] an integer indicating which axis should be distributed.
      bshape (tuple): The shape to which the input will ultimately be broadcast

    Returns:
      array_like or RemoteArray or DistArray or scalar
    """
    if (not hasattr(type(obj), '__array_interface__') and
            not isinstance(obj, Remote) and
            (isinstance(obj, string_types) or
             not isinstance(obj, Sequence))):
        # then treat it as a scalar
        return obj
    from distob import engine
    this_engine = engine.eid
    if location == this_engine:
        # move obj to the local host, if not already here
        if isinstance(obj, Remote) or isinstance(obj, DistArray):
            return gather(obj)
        else:
            return obj
    elif isinstance(location, numbers.Integral):
        # move obj to a single remote engine
        if isinstance(obj, Remote) and obj._ref.id.engine == location:
            #print('no data movement needed!')
            return obj
        obj = gather(obj)
        return _directed_scatter(obj, axis=None, destination=location)
    else:
        # location is a tuple (list of engine ids, distaxis) indicating that
        # obj should be distributed.
        engine_ids, distaxis = location
        if not isinstance(obj, DistArray):
            gather(obj)
            if isinstance(obj, Sequence):
                obj = np.array(obj)
        if obj.ndim < len(bshape):
            ix = (np.newaxis,)*(len(bshape)-obj.ndim) + (slice(None),)*obj.ndim
            obj = obj[ix]
        if (isinstance(obj, DistArray) and distaxis == obj._distaxis and
                engine_ids == [ra._ref.id.engine for ra in obj._subarrays]):
            #print('no data movement needed!')
            return obj
        obj = gather(obj)
        if obj.shape[distaxis] == 1:
            # broadcast this axis across engines
            subarrays = [_directed_scatter(obj, None, m) for m in engine_ids]
            return DistArray(subarrays, distaxis)
        else:
            return _directed_scatter(obj, distaxis, destination=engine_ids)