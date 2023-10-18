def ADD(cpu, dest, src):
        """
        Add.

        Adds the first operand (destination operand) and the second operand (source operand)
        and stores the result in the destination operand. When an immediate value is used as
        an operand, it is sign-extended to the length of the destination operand format.
        The ADD instruction does not distinguish between signed or unsigned operands. Instead,
        the processor evaluates the result for both data types and sets the OF and CF flags to
        indicate a carry in the signed or unsigned result, respectively. The SF flag indicates
        the sign of the signed result::

                DEST  =  DEST + SRC;

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        cpu._ADD(dest, src, carry=False)