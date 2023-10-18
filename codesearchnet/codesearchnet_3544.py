def cmp_regs(cpu, should_print=False):
    """
    Compare registers from a remote gdb session to current mcore.

    :param manticore.core.cpu Cpu: Current cpu
    :param bool should_print: Whether to print values to stdout
    :return: Whether or not any differences were detected
    :rtype: bool
    """
    differing = False
    gdb_regs = gdb.getCanonicalRegisters()
    for name in sorted(gdb_regs):
        vg = gdb_regs[name]
        if name.endswith('psr'):
            name = 'apsr'
        v = cpu.read_register(name.upper())
        if should_print:
            logger.debug(f'{name} gdb:{vg:x} mcore:{v:x}')
        if vg != v:
            if should_print:
                logger.warning('^^ unequal')
            differing = True
    if differing:
        logger.debug(qemu.correspond(None))
    return differing