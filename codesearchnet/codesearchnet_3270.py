def JNB(cpu, target):
        """
        Jumps short if not below.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, cpu.CF == False, target.read(), cpu.PC)