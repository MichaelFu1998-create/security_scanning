def INT(cpu, op0):
        """
        Calls to interrupt procedure.

        The INT n instruction generates a call to the interrupt or exception handler specified
        with the destination operand. The INT n instruction is the  general mnemonic for executing
        a software-generated call to an interrupt handler. The INTO instruction is a special
        mnemonic for calling overflow exception (#OF), interrupt vector number 4. The overflow
        interrupt checks the OF flag in the EFLAGS register and calls the overflow interrupt handler
        if the OF flag is set to 1.

        :param cpu: current CPU.
        :param op0: destination operand.
        """
        if op0.read() != 0x80:
            logger.warning("Unsupported interrupt")
        raise Interruption(op0.read())