def _commandline(self, *args, **kwargs):
        """Returns the command line (without pipes) as a list. Inserts driver if present"""
        if(self.driver is not None):
            return [self.driver, self.command_name] + self.transform_args(*args, **kwargs)
        return [self.command_name] + self.transform_args(*args, **kwargs)