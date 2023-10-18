def CDQ(cpu):
        """
        EDX:EAX = sign-extend of EAX
        """
        cpu.EDX = Operators.EXTRACT(Operators.SEXTEND(cpu.EAX, 32, 64), 32, 32)