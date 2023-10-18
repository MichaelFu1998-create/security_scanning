def CWDE(cpu):
        """
        Converts word to doubleword.

        ::
            DX = sign-extend of AX.

        :param cpu: current CPU.
        """
        bit = Operators.EXTRACT(cpu.AX, 15, 1)
        cpu.EAX = Operators.SEXTEND(cpu.AX, 16, 32)
        cpu.EDX = Operators.SEXTEND(bit, 1, 32)