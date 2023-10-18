def keys(self):
        """List names of options and positional arguments."""
        return self.options.keys() + [p.name for p in self.positional_args]