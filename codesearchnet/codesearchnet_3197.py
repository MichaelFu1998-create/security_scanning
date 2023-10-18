def ADC(cpu, dest, src):
        """
        Adds with carry.

        Adds the destination operand (first operand), the source operand (second operand),
        and the carry (CF) flag and stores the result in the destination operand. The state
        of the CF flag represents a carry from a previous addition. When an immediate value
        is used as an operand, it is sign-extended to the length of the destination operand
        format. The ADC instruction does not distinguish between signed or unsigned operands.
        Instead, the processor evaluates the result for both data types and sets the OF and CF
        flags to indicate a carry in the signed or unsigned result, respectively. The SF flag
        indicates the sign of the signed result. The ADC instruction is usually executed as
        part of a multibyte or multiword addition in which an ADD instruction is followed by an
        ADC instruction::

                DEST  =  DEST + SRC + CF;

        The OF, SF, ZF, AF, CF, and PF flags are set according to the result.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        cpu._ADD(dest, src, carry=True)