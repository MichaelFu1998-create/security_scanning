def _ufunc_dispatch(ufunc, method, i, inputs, **kwargs):
    """Route ufunc execution intelligently to local host or remote engine(s)
    depending on where the inputs are, to minimize the need to move data.
    Args:
      see numpy documentation for __numpy_ufunc__
    """
    #__print_ufunc(ufunc, method, i, inputs, **kwargs)
    if 'out' in kwargs and kwargs['out'] is not None:
        raise Error('for distributed ufuncs `out=` is not yet implemented')
    nin = 2 if ufunc is np.dot else ufunc.nin
    if nin is 1 and method == '__call__':
        return vectorize(ufunc.__call__)(inputs[0], **kwargs)
    elif nin is 2 and method == '__call__':
        from distob import engine
        here = engine.eid
        # Choose best location for the computation, possibly distributed:
        locs, weights = zip(*[_engine_affinity(a) for a in inputs])
        # for DistArrays, adjust preferred distaxis to account for broadcasting
        bshape = _broadcast_shape(*inputs)
        locs = list(locs)
        for i, loc in enumerate(locs):
            if isinstance(loc, _TupleType):
                num_new_axes = len(bshape) - inputs[i].ndim
                if num_new_axes > 0:
                    locs[i] = (locs[i][0], locs[i][1] + num_new_axes)
        if ufunc is np.dot:
            locs = [here if isinstance(m, _TupleType) else m for m in locs]
        if locs[0] == locs[1]:
            location = locs[0]
        else:
            # TODO: More accurately penalize the increased data movement if we
            # choose to distribute an axis that requires broadcasting.
            smallest = 0 if weights[0] <= weights[1] else 1
            largest = 1 - smallest
            if locs[0] is here or locs[1] is here:
                location = here if weights[0] == weights[1] else locs[largest]
            else:
                # Both inputs are on remote engines. With the current
                # implementation, data on one remote engine can only be moved
                # to another remote engine via the client. Cost accordingly:
                if weights[smallest]*2 < weights[largest] + weights[smallest]:
                    location = locs[largest]
                else:
                    location = here
        # Move both inputs to the chosen location:
        inputs = [_ufunc_move_input(a, location, bshape) for a in inputs]
        # Execute computation:
        if location is here:
            return ufunc.__call__(inputs[0], inputs[1], **kwargs)
        else:
            if isinstance(location, numbers.Integral):
                # location is a single remote engine
                return call(ufunc.__call__, inputs[0], inputs[1], **kwargs)
            else:
                # location is a tuple (list of engine ids, distaxis) implying
                # that the moved inputs are now distributed arrays (or scalar)
                engine_ids, distaxis = location
                n = len(engine_ids)
                is_dist = tuple(isinstance(a, DistArray) for a in inputs)
                assert(is_dist[0] or is_dist[1])
                for i in 0, 1:
                    if is_dist[i]:
                        ndim = inputs[i].ndim
                        assert(inputs[i]._distaxis == distaxis)
                        assert(inputs[i]._n == n)
                def _remote_ucall(inputs, **kwargs):
                    """(Executed on a remote or local engine) call the ufunc"""
                    return ufunc.__call__(inputs[0], inputs[1], **kwargs)
                results = []
                kwargs = kwargs.copy()
                kwargs['block'] = False
                kwargs['prefer_local'] = False
                for j in range(n):
                    subinputs = tuple(inputs[i]._subarrays[j] if 
                            is_dist[i] else inputs[i] for i in (0, 1))
                    results.append(call(_remote_ucall, subinputs, **kwargs))
                results = [convert_result(ar) for ar in results]
                return DistArray(results, distaxis)
    elif ufunc.nin > 2:
        raise Error(u'Distributing ufuncs with >2 inputs is not yet supported')
    else:
        raise Error(u'Distributed ufunc.%s() is not yet implemented' % method)