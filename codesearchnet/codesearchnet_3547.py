def initialize(state):
    """
    Synchronize the stack and register state (manticore->qemu)
    """
    logger.debug(f"Copying {stack_top - state.cpu.SP} bytes in the stack..")
    stack_bottom = min(state.cpu.SP, gdb.getR('SP'))
    for address in range(stack_bottom, stack_top):
        b = state.cpu.read_int(address, 8)
        gdb.setByte(address, chr(b))

    logger.debug("Done")

    # Qemu fd's start at 5, ours at 3. Add two filler fds
    mcore_stdout = state.platform.files[1]
    state.platform.files.append(mcore_stdout)
    state.platform.files.append(mcore_stdout)

    # Sync gdb's regs
    for gdb_reg in gdb.getCanonicalRegisters():
        if gdb_reg.endswith('psr'):
            mcore_reg = 'APSR'
        else:
            mcore_reg = gdb_reg.upper()
        value = state.cpu.read_register(mcore_reg)
        gdb.setR(gdb_reg, value)