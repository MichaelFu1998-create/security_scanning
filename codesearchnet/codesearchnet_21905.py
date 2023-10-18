def call_all(sequence, method_name, *args, **kwargs):
    """Call a method on each element of a sequence, in parallel.
    Returns:
      list of results
    """
    kwargs = kwargs.copy()
    kwargs['block'] = False
    results = []
    for obj in sequence:
        results.append(methodcall(obj, method_name, *args, **kwargs))
    for i in range(len(results)):
        results[i] = convert_result(results[i])
    return results