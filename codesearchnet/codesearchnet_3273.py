def JNO(cpu, target):
        """
        Jumps short if not overflow.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, False == cpu.OF, target.read(), cpu.PC)