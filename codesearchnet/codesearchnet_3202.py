def DAA(cpu):
        """
        Decimal adjusts AL after addition.

        Adjusts the sum of two packed BCD values to create a packed BCD result. The AL register
        is the implied source and destination operand. If a decimal carry is detected, the CF
        and AF flags are set accordingly.
        The CF and AF flags are set if the adjustment of the value results in a decimal carry in
        either digit of the result. The SF, ZF, and PF flags are set according to the result.

        This instruction is not valid in 64-bit mode.::

                IF (((AL AND 0FH) > 9) or AF  =  1)
                THEN
                    AL  =  AL + 6;
                    CF  =  CF OR CarryFromLastAddition; (* CF OR carry from AL  =  AL + 6 *)
                    AF  =  1;
                ELSE
                    AF  =  0;
                FI;
                IF ((AL AND F0H) > 90H) or CF  =  1)
                THEN
                    AL  =  AL + 60H;
                    CF  =  1;
                ELSE
                    CF  =  0;
                FI;

        :param cpu: current CPU.
        """

        cpu.AF = Operators.OR((cpu.AL & 0x0f) > 9, cpu.AF)
        oldAL = cpu.AL
        cpu.AL = Operators.ITEBV(8, cpu.AF, cpu.AL + 6, cpu.AL)
        cpu.CF = Operators.ITE(cpu.AF, Operators.OR(cpu.CF, cpu.AL < oldAL), cpu.CF)

        cpu.CF = Operators.OR((cpu.AL & 0xf0) > 0x90, cpu.CF)
        cpu.AL = Operators.ITEBV(8, cpu.CF, cpu.AL + 0x60, cpu.AL)
        """
        #old not-symbolic aware version...
        if ((cpu.AL & 0x0f) > 9) or cpu.AF:
            oldAL = cpu.AL
            cpu.AL =  cpu.AL + 6
            cpu.CF = Operators.OR(cpu.CF, cpu.AL < oldAL)
            cpu.AF  =  True
        else:
            cpu.AF  =  False

        if ((cpu.AL & 0xf0) > 0x90) or cpu.CF:
            cpu.AL  = cpu.AL + 0x60
            cpu.CF  =  True
        else:
            cpu.CF  =  False
        """

        cpu.ZF = cpu.AL == 0
        cpu.SF = (cpu.AL & 0x80) != 0
        cpu.PF = cpu._calculate_parity_flag(cpu.AL)