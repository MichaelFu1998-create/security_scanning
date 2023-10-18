def disassemble_instruction(self, code, pc):
        """Get next instruction using the Capstone disassembler

        :param str code: binary blob to be disassembled
        :param long pc: program counter
        """
        return next(self.disasm.disasm(code, pc))