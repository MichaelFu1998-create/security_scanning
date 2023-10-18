def run(self, cmd, *args, **kwargs):
        """Run a command."""
        runner = self.ctx.run if self.ctx else None
        return run(cmd, runner=runner, *args, **kwargs)