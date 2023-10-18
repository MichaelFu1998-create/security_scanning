def SETNG(cpu, dest):
        """
        Sets byte if not greater.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, Operators.OR(cpu.ZF, cpu.SF != cpu.OF), 1, 0))