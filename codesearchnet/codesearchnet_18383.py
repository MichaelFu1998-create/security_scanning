def items(self):
        """List values of options and positional arguments."""
        return [(p.name, p.value) for p in self.options.values() + self.positional_args]