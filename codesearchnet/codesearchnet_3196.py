def AAS(cpu):
        """
        ASCII Adjust AL after subtraction.

        Adjusts the result of the subtraction of two unpacked BCD values to  create a unpacked
        BCD result. The AL register is the implied source and destination operand for this instruction.
        The AAS instruction is only useful when it follows a SUB instruction that subtracts
        (binary subtraction) one unpacked BCD value from another and stores a byte result in the AL
        register. The AAA instruction then adjusts the contents of the AL register to contain the
        correct 1-digit unpacked BCD result. If the subtraction produced a decimal carry, the AH register
        is decremented by 1, and the CF and AF flags are set. If no decimal carry occurred, the CF and AF
        flags are cleared, and the AH register is unchanged. In either case, the AL register is left with
        its top nibble set to 0.

        The AF and CF flags are set to 1 if there is a decimal borrow; otherwise, they are cleared to 0.

        This instruction executes as described in compatibility mode and legacy mode.
        It is not valid in 64-bit mode.::


                IF ((AL AND 0FH) > 9) Operators.OR(AF  =  1)
                THEN
                    AX  =  AX - 6;
                    AH  =  AH - 1;
                    AF  =  1;
                    CF  =  1;
                ELSE
                    CF  =  0;
                    AF  =  0;
                FI;
                AL  =  AL AND 0FH;

        :param cpu: current CPU.
        """
        if (cpu.AL & 0x0F > 9) or cpu.AF == 1:
            cpu.AX = cpu.AX - 6
            cpu.AH = cpu.AH - 1
            cpu.AF = True
            cpu.CF = True
        else:
            cpu.AF = False
            cpu.CF = False
        cpu.AL = cpu.AL & 0x0f