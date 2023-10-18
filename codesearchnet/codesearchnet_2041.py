def match(self, context):
        """Returns True if the current context matches, False if it doesn't and
        None if matching is not finished, ie must be resumed after child
        contexts have been matched."""
        while context.remaining_codes() > 0 and context.has_matched is None:
            opcode = context.peek_code()
            if not self.dispatch(opcode, context):
                return None
        if context.has_matched is None:
            context.has_matched = False
        return context.has_matched