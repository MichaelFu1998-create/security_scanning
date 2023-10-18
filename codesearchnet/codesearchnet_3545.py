def post_mcore(state, last_instruction):
    """
    Handle syscalls (import memory) and bail if we diverge
    """
    global in_helper

    # Synchronize qemu state to manticore's after a system call
    if last_instruction.mnemonic.lower() == 'svc':
        # Synchronize all writes that have happened
        writes = state.cpu.memory.pop_record_writes()
        if writes:
            logger.debug("Got %d writes", len(writes))
        for addr, val in writes:
            gdb.setByte(addr, val[0])

        # Write return val to gdb
        gdb_r0 = gdb.getR('R0')
        if gdb_r0 != state.cpu.R0:
            logger.debug(f"Writing 0x{state.cpu.R0:x} to R0 (overwriting 0x{gdb.getR('R0'):x})")
        for reg in state.cpu.canonical_registers:
            if reg.endswith('PSR') or reg in ('R15', 'PC'):
                continue
            val = state.cpu.read_register(reg)
            gdb.setR(reg, val)


    # Ignore Linux kernel helpers
    if (state.cpu.PC >> 16) == 0xffff:
        in_helper = True
        return

    # If we executed a few instructions of a helper, we need to sync Manticore's
    # state to GDB as soon as we stop executing a helper.
    if in_helper:
        for reg in state.cpu.canonical_registers:
            if reg.endswith('PSR'):
                continue
            # Don't sync pc
            if reg == 'R15':
                continue
            gdb.setR(reg, state.cpu.read_register(reg))
        in_helper = False

    if cmp_regs(state.cpu):
        cmp_regs(state.cpu, should_print=True)
        state.abandon()