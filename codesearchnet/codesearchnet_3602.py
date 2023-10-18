def JUMPI(self, dest, cond):
        """Conditionally alter the program counter"""
        self.pc = Operators.ITEBV(256, cond != 0, dest, self.pc + self.instruction.size)
        #This set ups a check for JMPDEST in the next instruction if cond != 0
        self._set_check_jmpdest(cond != 0)