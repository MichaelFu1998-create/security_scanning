def ANDN(cpu, dest, src1, src2):
        """Performs a bitwise logical AND of inverted second operand (the first source operand)
           with the third operand (the second source operand). The result is stored in the first
           operand (destination operand).

                DEST <- (NOT SRC1) bitwiseAND SRC2;
                SF <- DEST[OperandSize -1];
                ZF <- (DEST = 0);
           Flags Affected
                SF and ZF are updated based on result. OF and CF flags are cleared. AF and PF flags are undefined.
        """
        value = ~src1.read() & src2.read()
        dest.write(value)
        cpu.ZF = value == 0
        cpu.SF = (value & (1 << dest.size)) != 0
        cpu.OF = False
        cpu.CF = False