def dispatch(self, opcode, context):
        """Dispatches a context on a given opcode. Returns True if the context
        is done matching, False if it must be resumed when next encountered."""
        if id(context) in self.executing_contexts:
            generator = self.executing_contexts[id(context)]
            del self.executing_contexts[id(context)]
            has_finished = generator.next()
        else:
            method = self.DISPATCH_TABLE.get(opcode, _OpcodeDispatcher.unknown)
            has_finished = method(self, context)
            if hasattr(has_finished, "next"): # avoid using the types module
                generator = has_finished
                has_finished = generator.next()
        if not has_finished:
            self.executing_contexts[id(context)] = generator
        return has_finished