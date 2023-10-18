def vectorize(f):
    """Upgrade normal function f to act in parallel on distibuted lists/arrays

    Args:
      f (callable): an ordinary function which expects as its first argument a
        single object, or a numpy array of N dimensions.

    Returns:
      vf (callable): new function that takes as its first argument a list of
        objects, or a array of N+1 dimensions. ``vf()`` will do the
        computation ``f()`` on each part of the input in parallel and will
        return a list of results, or a distributed array of results.
    """
    def vf(obj, *args, **kwargs):
        # user classes can customize how to vectorize a function:
        if hasattr(obj, '__distob_vectorize__'):
            return obj.__distob_vectorize__(f)(obj, *args, **kwargs)
        if isinstance(obj, Remote):
            return call(f, obj, *args, **kwargs)
        elif distob._have_numpy and (isinstance(obj, np.ndarray) or
                 hasattr(type(obj), '__array_interface__')):
            distarray = scatter(obj, axis=-1)
            return vf(distarray, *args, **kwargs)
        elif isinstance(obj, collections.Sequence):
            inputs = scatter(obj)
            dv = distob.engine._client[:]
            kwargs = kwargs.copy()
            kwargs['block'] = False
            results = []
            for obj in inputs:
                results.append(call(f, obj, *args, **kwargs))
            for i in range(len(results)):
                results[i] = convert_result(results[i])
            return results
    if hasattr(f, '__name__'):
        vf.__name__ = 'v' + f.__name__
        f_str = f.__name__ + '()'
    else:
        f_str = 'callable'
    doc = u"""Apply %s in parallel to a list or array\n
           Args:
             obj (Sequence of objects or an array)
             other args are the same as for %s
           """ % (f_str, f_str)
    if hasattr(f, '__doc__') and f.__doc__ is not None:
        doc = doc.rstrip() + (' detailed below:\n----------\n' + f.__doc__)
    vf.__doc__ = doc
    return vf