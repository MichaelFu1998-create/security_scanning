def SBB(cpu, dest, src):
        """
        Integer subtraction with borrow.

        Adds the source operand (second operand) and the carry (CF) flag, and
        subtracts the result from the destination operand (first operand). The
        result of the subtraction is stored in the destination operand. The
        destination operand can be a register or a memory location; the source
        operand can be an immediate, a register, or a memory location.
        (However, two memory operands cannot be used in one instruction.) The
        state of the CF flag represents a borrow from a previous subtraction.
        When an immediate value is used as an operand, it is sign-extended to
        the length of the destination operand format.
        The SBB instruction does not distinguish between signed or unsigned
        operands. Instead, the processor evaluates the result for both data
        types and sets the OF and CF flags to indicate a borrow in the signed
        or unsigned result, respectively. The SF flag indicates the sign of the
        signed result.  The SBB instruction is usually executed as part of a
        multibyte or multiword subtraction in which a SUB instruction is
        followed by a SBB instruction::

                DEST  =  DEST - (SRC + CF);

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        cpu._SUB(dest, src, carry=True)