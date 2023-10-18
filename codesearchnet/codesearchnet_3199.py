def CMP(cpu, src1, src2):
        """
        Compares two operands.

        Compares the first source operand with the second source operand and sets the status flags
        in the EFLAGS register according to the results. The comparison is performed by subtracting
        the second operand from the first operand and then setting the status flags in the same manner
        as the SUB instruction. When an immediate value is used as an operand, it is sign-extended to
        the length of the first operand::

                temp  =  SRC1 - SignExtend(SRC2);
                ModifyStatusFlags; (* Modify status flags in the same manner as the SUB instruction*)

        The CF, OF, SF, ZF, AF, and PF flags are set according to the result.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        arg0 = src1.read()
        arg1 = Operators.SEXTEND(src2.read(), src2.size, src1.size)

        # Affected Flags o..szapc
        cpu._calculate_CMP_flags(src1.size, arg0 - arg1, arg0, arg1)