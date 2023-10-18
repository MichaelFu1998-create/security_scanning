def LJMP(cpu, cs_selector, target):
        """
        We are just going to ignore the CS selector for now.
        """
        logger.info("LJMP: Jumping to: %r:%r", cs_selector.read(), target.read())
        cpu.CS = cs_selector.read()
        cpu.PC = target.read()