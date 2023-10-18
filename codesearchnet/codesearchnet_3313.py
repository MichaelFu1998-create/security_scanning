def CQO(cpu):
        """
        RDX:RAX = sign-extend of RAX.
        """
        res = Operators.SEXTEND(cpu.RAX, 64, 128)
        cpu.RAX = Operators.EXTRACT(res, 0, 64)
        cpu.RDX = Operators.EXTRACT(res, 64, 64)