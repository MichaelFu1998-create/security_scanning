def ADDW(cpu, dest, src, add):
        """
        This instruction adds an immediate value to a register value, and writes the result to the destination register.
        It doesn't update the condition flags.

        :param ARMv7Operand dest: Specifies the destination register. If omitted, this register is the same as src.
        :param ARMv7Operand src:
            Specifies the register that contains the first operand. If the SP is specified for dest, see ADD (SP plus
            immediate). If the PC is specified for dest, see ADR.
        :param ARMv7Operand add:
            Specifies the immediate value to be added to the value obtained from src. The range of allowed values is
            0-4095.
        """
        aligned_pc = (cpu.instruction.address + 4) & 0xfffffffc
        if src.type == 'register' and src.reg in ('PC', 'R15'):
            src = aligned_pc
        else:
            src = src.read()
        dest.write(src + add.read())