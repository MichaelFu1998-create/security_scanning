def ADR(cpu, dest, src):
        """
        Address to Register adds an immediate value to the PC value, and writes the result to the destination register.

        :param ARMv7Operand dest: Specifies the destination register.
        :param ARMv7Operand src:
            Specifies the label of an instruction or literal data item whose address is to be loaded into
            <Rd>. The assembler calculates the required value of the offset from the Align(PC,4)
            value of the ADR instruction to this label.
        """
        aligned_pc = (cpu.instruction.address + 4) & 0xfffffffc
        dest.write(aligned_pc + src.read())