def run(self, ctx):
        """
        Runs the current phase.
        """
        # Reverse engine assertion if needed
        if ctx.reverse:
            self.engine.reverse()

        if self.engine.empty:
            raise AssertionError('grappa: no assertions to run')

        try:
            # Run assertion in series and return error, if present
            return self.run_assertions(ctx)
        except Exception as _err:
            # Handle legit grappa internval errors
            if getattr(_err, '__legit__', False):
                raise _err
            # Otherwise render it
            return self.render_error(ctx, _err)