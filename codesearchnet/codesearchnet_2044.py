def count_repetitions(self, ctx, maxcount):
        """Returns the number of repetitions of a single item, starting from the
        current string position. The code pointer is expected to point to a
        REPEAT_ONE operation (with the repeated 4 ahead)."""
        count = 0
        real_maxcount = ctx.state.end - ctx.string_position
        if maxcount < real_maxcount and maxcount != MAXREPEAT:
            real_maxcount = maxcount
        # XXX could special case every single character pattern here, as in C.
        # This is a general solution, a bit hackisch, but works and should be
        # efficient.
        code_position = ctx.code_position
        string_position = ctx.string_position
        ctx.skip_code(4)
        reset_position = ctx.code_position
        while count < real_maxcount:
            # this works because the single character pattern is followed by
            # a success opcode
            ctx.code_position = reset_position
            self.dispatch(ctx.peek_code(), ctx)
            if ctx.has_matched is False: # could be None as well
                break
            count += 1
        ctx.has_matched = None
        ctx.code_position = code_position
        ctx.string_position = string_position
        return count