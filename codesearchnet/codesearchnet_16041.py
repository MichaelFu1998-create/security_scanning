def compile(code: list, consts: list, names: list, varnames: list,
            func_name: str = "<unknown, compiled>",
            arg_count: int = 0, kwarg_defaults: Tuple[Any] = (), use_safety_wrapper: bool = True):
    """
    Compiles a set of bytecode instructions into a working function, using Python's bytecode
    compiler.

    :param code: A list of bytecode instructions.
    :param consts: A list of constants to compile into the function.
    :param names: A list of names to compile into the function.
    :param varnames: A list of ``varnames`` to compile into the function.
    :param func_name: The name of the function to use.
    :param arg_count: The number of arguments this function takes. Must be ``<= len(varnames)``.
    :param kwarg_defaults: A tuple of defaults for kwargs.
    :param use_safety_wrapper: Use the safety wrapper? This hijacks SystemError to print better \
        stack traces.
    """
    varnames = tuple(varnames)
    consts = tuple(consts)
    names = tuple(names)

    # Flatten the code list.
    code = util.flatten(code)

    if arg_count > len(varnames):
        raise CompileError("arg_count > len(varnames)")

    if len(kwarg_defaults) > len(varnames):
        raise CompileError("len(kwarg_defaults) > len(varnames)")

    # Compile it.
    bc = compile_bytecode(code)

    dis.dis(bc)

    # Check for a final RETURN_VALUE.
    if PY36:
        # TODO: Add Python 3.6 check
        pass
    else:
        if bc[-1] != tokens.RETURN_VALUE:
            raise CompileError(
                "No default RETURN_VALUE. Add a `pyte.tokens.RETURN_VALUE` to the end of your "
                "bytecode if you don't need one.")

    # Set default flags
    flags = 1 | 2 | 64

    frame_data = inspect.stack()[1]

    if sys.version_info[0:2] > (3, 3):
        # Validate the stack.
        stack_size = _simulate_stack(dis._get_instructions_bytes(
            bc, constants=consts, names=names, varnames=varnames)
        )
    else:
        warnings.warn("Cannot check stack for safety.")
        stack_size = 99

    # Generate optimization warnings.
    _optimize_warn_pass(dis._get_instructions_bytes(bc, constants=consts, names=names, varnames=varnames))

    obb = types.CodeType(
        arg_count,  # Varnames - used for arguments.
        0,  # Kwargs are not supported yet
        len(varnames),  # co_nlocals -> Non-argument local variables
        stack_size,  # Auto-calculated
        flags,  # 67 is default for a normal function.
        bc,  # co_code - use the bytecode we generated.
        consts,  # co_consts
        names,  # co_names, used for global calls.
        varnames,  # arguments
        frame_data[1],  # use <unknown, compiled>
        func_name,  # co_name
        frame_data[2],  # co_firstlineno, ignore this.
        b'',  # https://svn.python.org/projects/python/trunk/Objects/lnotab_notes.txt
        (),  # freevars - no idea what this does
        ()  # cellvars - used for nested functions - we don't use these.
    )
    # Update globals
    f_globals = frame_data[0].f_globals

    # Create a function type.
    f = types.FunctionType(obb, f_globals)
    f.__name__ = func_name
    f.__defaults__ = kwarg_defaults

    if use_safety_wrapper:
        def __safety_wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except SystemError as e:
                if 'opcode' not in ' '.join(e.args):
                    # Re-raise any non opcode related errors.
                    raise
                msg = "Bytecode exception!" \
                      "\nFunction {} returned an invalid opcode." \
                      "\nFunction dissection:\n\n".format(f.__name__)
                # dis sucks and always prints to stdout
                # so we capture it
                file = io.StringIO()
                with contextlib.redirect_stdout(file):
                    dis.dis(f)
                msg += file.getvalue()
                raise SystemError(msg) from e

        returned_func = __safety_wrapper
        returned_func.wrapped = f
    else:
        returned_func = f

    # return the func
    return returned_func