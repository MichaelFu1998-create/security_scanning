def TEST(cpu, src1, src2):
        """
        Logical compare.

        Computes the bit-wise logical AND of first operand (source 1 operand)
        and the second operand (source 2 operand) and sets the SF, ZF, and PF
        status flags according to the result. The result is then discarded::

            TEMP  =  SRC1 AND SRC2;
            SF  =  MSB(TEMP);
            IF TEMP  =  0
            THEN ZF  =  1;
            ELSE ZF  =  0;
            FI:
            PF  =  BitwiseXNOR(TEMP[0:7]);
            CF  =  0;
            OF  =  0;
            (*AF is Undefined*)

        :param cpu: current CPU.
        :param src1: first operand.
        :param src2: second operand.
        """
        # Defined Flags: szp
        temp = src1.read() & src2.read()
        cpu.SF = (temp & (1 << (src1.size - 1))) != 0
        cpu.ZF = temp == 0
        cpu.PF = cpu._calculate_parity_flag(temp)
        cpu.CF = False
        cpu.OF = False