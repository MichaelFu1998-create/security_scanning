def AAD(cpu, imm=None):
        """
        ASCII adjust AX before division.

        Adjusts two unpacked BCD digits (the least-significant digit in the
        AL register and the most-significant digit in the AH register) so that
        a division operation performed on the result will yield a correct unpacked
        BCD value. The AAD instruction is only useful when it precedes a DIV instruction
        that divides (binary division) the adjusted value in the AX register by
        an unpacked BCD value.
        The AAD instruction sets the value in the AL register to (AL + (10 * AH)), and then
        clears the AH register to 00H. The value in the AX register is then equal to the binary
        equivalent of the original unpacked two-digit (base 10) number in registers AH and AL.

        The SF, ZF, and PF flags are set according to the resulting binary value in the AL register.

        This instruction executes as described in compatibility mode and legacy mode.
        It is not valid in 64-bit mode.::

                tempAL  =  AL;
                tempAH  =  AH;
                AL  =  (tempAL + (tempAH * 10)) AND FFH;
                AH  =  0

        :param cpu: current CPU.
        """
        if imm is None:
            imm = 10
        else:
            imm = imm.read()

        cpu.AL += cpu.AH * imm
        cpu.AH = 0

        # Defined flags: ...sz.p.
        cpu._calculate_logic_flags(8, cpu.AL)