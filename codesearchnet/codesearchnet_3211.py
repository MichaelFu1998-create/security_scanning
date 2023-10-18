def SUB(cpu, dest, src):
        """
        Subtract.

        Subtracts the second operand (source operand) from the first operand
        (destination operand) and stores the result in the destination operand.
        The destination operand can be a register or a memory location; the
        source operand can be an immediate, register, or memory location.
        (However, two memory operands cannot be used in one instruction.) When
        an immediate value is used as an operand, it is sign-extended to the
        length of the destination operand format.
        The SUB instruction does not distinguish between signed or unsigned
        operands. Instead, the processor evaluates the result for both
        data types and sets the OF and CF flags to indicate a borrow in the
        signed or unsigned result, respectively. The SF flag indicates the sign
        of the signed result::

            DEST  =  DEST - SRC;

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        cpu._SUB(dest, src, carry=False)