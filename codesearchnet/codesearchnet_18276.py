def get_pickling_errors(obj, seen=None):
    """Investigate pickling errors."""
    if seen == None:
        seen = []
    if hasattr(obj, "__getstate__"):
        state = obj.__getstate__()
    #elif hasattr(obj, "__dict__"):
    #    state = obj.__dict__
    else:
        return None
    #try:
    #    state = obj.__getstate__()
    #except AttributeError as e:
    #    #state = obj.__dict__
    #    return str(e)
    if state == None:
        return 'object state is None'
    if isinstance(state,tuple):
        if not isinstance(state[0], dict):
            state=state[1]
        else:
            state=state[0].update(state[1])
    result = {}
    for i in state:
        try:
            pickle.dumps(state[i], protocol=2)
        except pickle.PicklingError as e:
            if not state[i] in seen:
                seen.append(state[i])
                result[i]=get_pickling_errors(state[i],seen)
    return result