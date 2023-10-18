def OR(cpu, dest, src):
        """
        Logical inclusive OR.

        Performs a bitwise inclusive OR operation between the destination (first)
        and source (second) operands and stores the result in the destination operand location.

        Each bit of the result of the OR instruction is set to 0 if both corresponding
        bits of the first and second operands are 0; otherwise, each bit is set
        to 1.

        The OF and CF flags are cleared; the SF, ZF, and PF flags are set according to the result::

            DEST  =  DEST OR SRC;

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        res = dest.write(dest.read() | src.read())
        # Defined Flags: szp
        cpu._calculate_logic_flags(dest.size, res)