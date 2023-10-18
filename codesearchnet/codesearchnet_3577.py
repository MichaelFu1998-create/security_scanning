def _checkpoint(self):
        """Save and/or get a state checkpoint previous to current instruction"""
        #Fixme[felipe] add a with self.disabled_events context mangr to Eventful
        if self._checkpoint_data is None:
            if not self._published_pre_instruction_events:
                self._published_pre_instruction_events = True
                self._publish('will_decode_instruction', self.pc)
                self._publish('will_execute_instruction', self.pc, self.instruction)
                self._publish('will_evm_execute_instruction', self.instruction, self._top_arguments())

            pc = self.pc
            instruction = self.instruction
            old_gas = self.gas
            allocated = self._allocated
            #FIXME Not clear which exception should trigger first. OOG or insuficient stack
            # this could raise an insuficient stack exception
            arguments = self._pop_arguments()
            fee = self._calculate_gas(*arguments)
            self._checkpoint_data = (pc, old_gas, instruction, arguments, fee, allocated)
        return self._checkpoint_data