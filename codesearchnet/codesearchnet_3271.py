def JNE(cpu, target):
        """
        Jumps short if not equal.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, False == cpu.ZF, target.read(), cpu.PC)