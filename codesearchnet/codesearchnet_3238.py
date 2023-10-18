def SETGE(cpu, dest):
        """
        Sets byte if greater or equal.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.SF == cpu.OF, 1, 0))