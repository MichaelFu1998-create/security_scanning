def AAM(cpu, imm=None):
        """
        ASCII adjust AX after multiply.

        Adjusts the result of the multiplication of two unpacked BCD values
        to create a pair of unpacked (base 10) BCD values. The AX register is
        the implied source and destination operand for this instruction. The AAM
        instruction is only useful when it follows a MUL instruction that multiplies
        (binary multiplication) two unpacked BCD values and stores a word result
        in the AX register. The AAM instruction then adjusts the contents of the
        AX register to contain the correct 2-digit unpacked (base 10) BCD result.

        The SF, ZF, and PF flags are set according to the resulting binary value in the AL register.

        This instruction executes as described in compatibility mode and legacy mode.
        It is not valid in 64-bit mode.::

                tempAL  =  AL;
                AH  =  tempAL / 10;
                AL  =  tempAL MOD 10;

        :param cpu: current CPU.
        """
        if imm is None:
            imm = 10
        else:
            imm = imm.read()

        cpu.AH = Operators.UDIV(cpu.AL, imm)
        cpu.AL = Operators.UREM(cpu.AL, imm)

        # Defined flags: ...sz.p.
        cpu._calculate_logic_flags(8, cpu.AL)