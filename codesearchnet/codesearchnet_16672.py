def get_node(obj, args, kwargs):
    """Create a node from arguments and return it"""

    if args is None and kwargs is None:
        return (obj,)

    if kwargs is None:
        kwargs = {}
    return obj, _bind_args(obj, args, kwargs)