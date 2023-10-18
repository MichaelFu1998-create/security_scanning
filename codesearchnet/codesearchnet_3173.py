def _publish_instruction_as_executed(self, insn):
        """
        Notify listeners that an instruction has been executed.
        """
        self._icount += 1
        self._publish('did_execute_instruction', self._last_pc, self.PC, insn)