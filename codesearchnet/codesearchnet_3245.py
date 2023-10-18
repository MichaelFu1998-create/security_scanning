def SETNS(cpu, dest):
        """
        Sets byte if not sign.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.SF == False, 1, 0))