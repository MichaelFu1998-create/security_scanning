def CALL(cpu, op0):
        """
        Procedure call.

        Saves procedure linking information on the stack and branches to the called procedure specified using the target
        operand. The target operand specifies the address of the first instruction in the called procedure. The operand can
        be an immediate value, a general-purpose register, or a memory location.

        :param cpu: current CPU.
        :param op0: target operand.
        """
        # TODO FIX 64Bit FIX segment
        proc = op0.read()
        cpu.push(cpu.PC, cpu.address_bit_size)
        cpu.PC = proc