def _commandline(self, *args, **kwargs):
        """Returns the command line (without pipes) as a list."""
         # transform_args() is a hook (used in GromacsCommand very differently!)
        return [self.command_name] + self.transform_args(*args, **kwargs)