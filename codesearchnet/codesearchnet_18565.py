def register_default_types():
    """Regiser all default type-to-pipe convertors."""
    register_type(type, pipe.map)
    register_type(types.FunctionType, pipe.map)
    register_type(types.MethodType, pipe.map)
    register_type(tuple, seq)
    register_type(list, seq)
    register_type(types.GeneratorType, seq)
    register_type(string_type, sh)
    register_type(unicode_type, sh)
    register_type(file_type, fileobj)

    if is_py3:
        register_type(range, seq)
        register_type(map, seq)