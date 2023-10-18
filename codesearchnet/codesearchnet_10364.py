def _run_command(self,*args,**kwargs):
        """Execute the gromacs command; see the docs for __call__."""
        result, p = super(GromacsCommand, self)._run_command(*args, **kwargs)
        self.check_failure(result, command_string=p.command_string)
        return result, p