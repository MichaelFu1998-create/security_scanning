def sync_svc(state):
    """
    Mirror some service calls in manticore. Happens after qemu executed a SVC
    instruction, but before manticore did.
    """
    syscall = state.cpu.R7 # Grab idx from manticore since qemu could have exited
    name = linux_syscalls.armv7[syscall]

    logger.debug(f"Syncing syscall: {name}")

    try:
        # Make sure mmap returns the same address
        if 'mmap' in name:
            returned = gdb.getR('R0')
            logger.debug(f"Syncing mmap ({returned:x})")
            state.cpu.write_register('R0', returned)
        if 'exit' in name:
            return
    except ValueError:
        for reg in state.cpu.canonical_registers:
            print(f'{reg}: {state.cpu.read_register(reg):x}')
        raise