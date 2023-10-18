def _reg_name(self, reg_id):
        """
        Translates a register ID from the disassembler object into the
        register name based on manticore's alias in the register file

        :param int reg_id: Register ID
        """
        if reg_id >= X86_REG_ENDING:
            logger.warning("Trying to get register name for a non-register")
            return None
        cs_reg_name = self.cpu.instruction.reg_name(reg_id)
        if cs_reg_name is None or cs_reg_name.lower() == '(invalid)':
            return None
        return self.cpu._regfile._alias(cs_reg_name.upper())