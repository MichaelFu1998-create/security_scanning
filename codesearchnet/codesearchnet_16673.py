def node_get_args(node):
    """Return an ordered mapping from params to args"""
    obj = node[OBJ]
    key = node[KEY]
    boundargs = obj.formula.signature.bind(*key)
    boundargs.apply_defaults()
    return boundargs.arguments