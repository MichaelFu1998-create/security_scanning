def SETC(cpu, dest):
        """
        Sets if carry.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.CF, 1, 0))