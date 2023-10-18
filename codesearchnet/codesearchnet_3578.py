def _rollback(self):
        """Revert the stack, gas, pc and memory allocation so it looks like before executing the instruction"""
        last_pc, last_gas, last_instruction, last_arguments, fee, allocated = self._checkpoint_data
        self._push_arguments(last_arguments)
        self._gas = last_gas
        self._pc = last_pc
        self._allocated = allocated
        self._checkpoint_data = None