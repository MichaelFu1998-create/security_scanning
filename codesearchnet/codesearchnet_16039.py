def compile_bytecode(code: list) -> bytes:
    """
    Compiles Pyte objects into a bytecode list.

    :param code: A list of objects to compile.
    :return: The computed bytecode.
    """
    bc = b""
    for i, op in enumerate(code):
        try:
            # Get the bytecode.
            if isinstance(op, _PyteOp) or isinstance(op, _PyteAugmentedComparator):
                bc_op = op.to_bytes(bc)
            elif isinstance(op, int):
                bc_op = op.to_bytes(1, byteorder="little")
            elif isinstance(op, bytes):
                bc_op = op
            else:
                raise CompileError("Could not compile code of type {}".format(type(op)))
            bc += bc_op
        except Exception as e:
            print("Fatal compiliation error on operator {i} ({op}).".format(i=i, op=op))
            raise e

    return bc