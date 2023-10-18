def SETNLE(cpu, dest):
        """
        Sets byte if not less or equal.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, Operators.AND(cpu.ZF == False, cpu.SF == cpu.OF), 1, 0))