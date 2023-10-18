def AAA(cpu):
        """
        ASCII adjust after addition.

        Adjusts the sum of two unpacked BCD values to create an unpacked BCD
        result. The AL register is the implied source and destination operand
        for this instruction. The AAA instruction is only useful when it follows
        an ADD instruction that adds (binary addition) two unpacked BCD values
        and stores a byte result in the AL register. The AAA instruction then
        adjusts the contents of the AL register to contain the correct 1-digit
        unpacked BCD result.
        If the addition produces a decimal carry, the AH register is incremented
        by 1, and the CF and AF flags are set. If there was no decimal carry,
        the CF and AF flags are cleared and the AH register is unchanged. In either
        case, bits 4 through 7 of the AL register are cleared to 0.

        This instruction executes as described in compatibility mode and legacy mode.
        It is not valid in 64-bit mode.
        ::
                IF ((AL AND 0FH) > 9) Operators.OR(AF  =  1)
                THEN
                    AL  =  (AL + 6);
                    AH  =  AH + 1;
                    AF  =  1;
                    CF  =  1;
                ELSE
                    AF  =  0;
                    CF  =  0;
                FI;
                AL  =  AL AND 0FH;
        :param cpu: current CPU.
        """
        cpu.AF = Operators.OR(cpu.AL & 0x0F > 9, cpu.AF)
        cpu.CF = cpu.AF
        cpu.AH = Operators.ITEBV(8, cpu.AF, cpu.AH + 1, cpu.AH)
        cpu.AL = Operators.ITEBV(8, cpu.AF, cpu.AL + 6, cpu.AL)
        """
        if (cpu.AL & 0x0F > 9) or cpu.AF == 1:
            cpu.AL = cpu.AL + 6
            cpu.AH = cpu.AH + 1
            cpu.AF = True
            cpu.CF = True
        else:
            cpu.AF = False
            cpu.CF = False
        """
        cpu.AL = cpu.AL & 0x0f