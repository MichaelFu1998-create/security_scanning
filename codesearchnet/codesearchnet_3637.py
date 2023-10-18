def CBZ(cpu, op, dest):
        """
        Compare and Branch on Zero compares the value in a register with zero, and conditionally branches forward
        a constant value. It does not affect the condition flags.

        :param ARMv7Operand op: Specifies the register that contains the first operand.
        :param ARMv7Operand dest:
            Specifies the label of the instruction that is to be branched to. The assembler calculates the
            required value of the offset from the PC value of the CBZ instruction to this label, then
            selects an encoding that will set imm32 to that offset. Allowed offsets are even numbers in
            the range 0 to 126.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size,
                                 op.read(), cpu.PC, dest.read())