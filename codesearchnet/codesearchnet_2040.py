def push_new_context(self, pattern_offset):
        """Creates a new child context of this context and pushes it on the
        stack. pattern_offset is the offset off the current code position to
        start interpreting from."""
        child_context = _MatchContext(self.state,
            self.pattern_codes[self.code_position + pattern_offset:])
        self.state.context_stack.append(child_context)
        return child_context