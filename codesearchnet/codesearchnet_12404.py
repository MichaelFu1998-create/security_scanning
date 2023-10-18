def get_type_info(obj):
    """Get type information for a Python object

    Args:
        obj: The Python object

    Returns:
        tuple: (object type "catagory", object type name)
    """
    if isinstance(obj, primitive_types):
        return ('primitive', type(obj).__name__)
    if isinstance(obj, sequence_types):
        return ('sequence', type(obj).__name__)
    if isinstance(obj, array_types):
        return ('array', type(obj).__name__)
    if isinstance(obj, key_value_types):
        return ('key-value', type(obj).__name__)
    if isinstance(obj, types.ModuleType):
        return ('module', type(obj).__name__)
    if isinstance(obj, (types.FunctionType, types.MethodType)):
        return ('function', type(obj).__name__)
    if isinstance(obj, type):
        if hasattr(obj, '__dict__'):
            return ('class', obj.__name__)
    if isinstance(type(obj), type):
        if hasattr(obj, '__dict__'):
            cls_name = type(obj).__name__
            if cls_name == 'classobj':
                cls_name = obj.__name__
                return ('class', '{}'.format(cls_name))
            if cls_name == 'instance':
                cls_name = obj.__class__.__name__
            return ('instance', '{} instance'.format(cls_name))

    return ('unknown', type(obj).__name__)