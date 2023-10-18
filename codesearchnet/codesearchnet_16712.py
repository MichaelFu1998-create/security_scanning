def _alter_code(code, **attrs):
    """Create a new code object by altering some of ``code`` attributes

    Args:
        code: code objcect
        attrs: a mapping of names of code object attrs to their values
    """

    PyCode_New = ctypes.pythonapi.PyCode_New

    PyCode_New.argtypes = (
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.py_object,
        ctypes.py_object,
        ctypes.py_object,
        ctypes.py_object,
        ctypes.py_object,
        ctypes.py_object,
        ctypes.py_object,
        ctypes.py_object,
        ctypes.c_int,
        ctypes.py_object)

    PyCode_New.restype = ctypes.py_object

    args = [
        [code.co_argcount, 'co_argcount'],
        [code.co_kwonlyargcount, 'co_kwonlyargcount'],
        [code.co_nlocals, 'co_nlocals'],
        [code.co_stacksize, 'co_stacksize'],
        [code.co_flags, 'co_flags'],
        [code.co_code, 'co_code'],
        [code.co_consts, 'co_consts'],
        [code.co_names, 'co_names'],
        [code.co_varnames, 'co_varnames'],
        [code.co_freevars, 'co_freevars'],
        [code.co_cellvars, 'co_cellvars'],
        [code.co_filename, 'co_filename'],
        [code.co_name, 'co_name'],
        [code.co_firstlineno, 'co_firstlineno'],
        [code.co_lnotab, 'co_lnotab']]

    for arg in args:
        if arg[1] in attrs:
            arg[0] = attrs[arg[1]]

    return PyCode_New(
        args[0][0],  # code.co_argcount,
        args[1][0],  # code.co_kwonlyargcount,
        args[2][0],  # code.co_nlocals,
        args[3][0],  # code.co_stacksize,
        args[4][0],  # code.co_flags,
        args[5][0],  # code.co_code,
        args[6][0],  # code.co_consts,
        args[7][0],  # code.co_names,
        args[8][0],  # code.co_varnames,
        args[9][0],  # code.co_freevars,
        args[10][0],  # code.co_cellvars,
        args[11][0],  # code.co_filename,
        args[12][0],  # code.co_name,
        args[13][0],  # code.co_firstlineno,
        args[14][0])