def _instructions_changed(self, change):
        """Call when there is a change in the instructions."""
        if change.adds():
            for index, instruction in change.items():
                if isinstance(instruction, dict):
                    in_row = self._parser.instruction_in_row(self, instruction)
                    self.instructions[index] = in_row
                else:
                    instruction.transfer_to_row(self)