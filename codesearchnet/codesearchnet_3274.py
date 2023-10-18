def JNP(cpu, target):
        """
        Jumps short if not parity.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, False == cpu.PF, target.read(), cpu.PC)