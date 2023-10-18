def _finish_instructions(self):
        """Finish those who still need to inherit."""
        while self._instruction_todos:
            row = self._instruction_todos.pop()
            instructions = row.get(INSTRUCTIONS, [])
            row.instructions.extend(instructions)