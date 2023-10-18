def _simulate_stack(code: list) -> int:
    """
    Simulates the actions of the stack, to check safety.

    This returns the maximum needed stack.
    """

    max_stack = 0
    curr_stack = 0

    def _check_stack(ins):
        if curr_stack < 0:
            raise CompileError("Stack turned negative on instruction: {}".format(ins))
        if curr_stack > max_stack:
            return curr_stack

    # Iterate over the bytecode.
    for instruction in code:
        assert isinstance(instruction, dis.Instruction)
        if instruction.arg is not None:
            try:
                effect = dis.stack_effect(instruction.opcode, instruction.arg)
            except ValueError as e:
                raise CompileError("Invalid opcode `{}` when compiling"
                                   .format(instruction.opcode)) from e
        else:
            try:
                effect = dis.stack_effect(instruction.opcode)
            except ValueError as e:
                raise CompileError("Invalid opcode `{}` when compiling"
                                   .format(instruction.opcode)) from e
        curr_stack += effect
        # Re-check the stack.
        _should_new_stack = _check_stack(instruction)
        if _should_new_stack:
            max_stack = _should_new_stack

    return max_stack