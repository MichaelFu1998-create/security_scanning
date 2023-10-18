def DAS(cpu):
        """
        Decimal adjusts AL after subtraction.

        Adjusts the result of the subtraction of two packed BCD values to create a packed BCD result.
        The AL register is the implied source and destination operand. If a decimal borrow is detected,
        the CF and AF flags are set accordingly. This instruction is not valid in 64-bit mode.

        The SF, ZF, and PF flags are set according to the result.::

                IF (AL AND 0FH) > 9 OR AF  =  1
                THEN
                    AL  =  AL - 6;
                    CF  =  CF OR BorrowFromLastSubtraction; (* CF OR borrow from AL  =  AL - 6 *)
                    AF  =  1;
                ELSE
                    AF  =  0;
                FI;
                IF ((AL > 99H) or OLD_CF  =  1)
                THEN
                    AL  =  AL - 60H;
                    CF  =  1;

        :param cpu: current CPU.
        """
        oldAL = cpu.AL
        oldCF = cpu.CF

        cpu.AF = Operators.OR((cpu.AL & 0x0f) > 9, cpu.AF)
        cpu.AL = Operators.ITEBV(8, cpu.AF, cpu.AL - 6, cpu.AL)
        cpu.CF = Operators.ITE(cpu.AF, Operators.OR(oldCF, cpu.AL > oldAL), cpu.CF)

        cpu.CF = Operators.ITE(Operators.OR(oldAL > 0x99, oldCF), True, cpu.CF)
        cpu.AL = Operators.ITEBV(8, Operators.OR(oldAL > 0x99, oldCF), cpu.AL - 0x60, cpu.AL)
        #
        """
        if (cpu.AL & 0x0f) > 9 or cpu.AF:
            cpu.AL = cpu.AL - 6;
            cpu.CF = Operators.OR(oldCF, cpu.AL > oldAL)
            cpu.AF = True
        else:
            cpu.AF  =  False

        if ((oldAL > 0x99) or oldCF):
            cpu.AL = cpu.AL - 0x60
            cpu.CF = True
        """
        cpu.ZF = cpu.AL == 0
        cpu.SF = (cpu.AL & 0x80) != 0
        cpu.PF = cpu._calculate_parity_flag(cpu.AL)