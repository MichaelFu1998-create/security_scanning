def use_pickle():
    """Revert to using stdlib pickle.

    Reverts custom serialization enabled by use_dill|cloudpickle.
    """
    from . import serialize
    serialize.pickle = serialize._stdlib_pickle

    # restore special function handling
    can_map[FunctionType] = _original_can_map[FunctionType]