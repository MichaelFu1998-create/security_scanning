def check_charset(self, ctx, char):
        """Checks whether a character matches set of arbitrary length. Assumes
        the code pointer is at the first member of the set."""
        self.set_dispatcher.reset(char)
        save_position = ctx.code_position
        result = None
        while result is None:
            result = self.set_dispatcher.dispatch(ctx.peek_code(), ctx)
        ctx.code_position = save_position
        return result