def PTEST(cpu, dest, src):
        """ PTEST
         PTEST set the ZF flag if all bits in the result are 0 of the bitwise AND
         of the first source operand (first operand) and the second source operand
         (second operand). Also this sets the CF flag if all bits in the result
         are 0 of the bitwise AND of the second source operand (second operand)
         and the logical NOT of the destination operand.
        """
        cpu.OF = False
        cpu.AF = False
        cpu.PF = False
        cpu.SF = False
        cpu.ZF = (Operators.EXTRACT(dest.read(), 0, 128) & Operators.EXTRACT(src.read(), 0, 128)) == 0
        cpu.CF = (Operators.EXTRACT(src.read(), 0, 128) & ~(Operators.EXTRACT(dest.read(), 0, 128))) == 0