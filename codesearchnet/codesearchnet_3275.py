def JNS(cpu, target):
        """
        Jumps short if not sign.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, False == cpu.SF, target.read(), cpu.PC)