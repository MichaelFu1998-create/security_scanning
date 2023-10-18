def values(self):
        """List values of options and positional arguments."""
        return self.options.values() + [p.value for p in self.positional_args]