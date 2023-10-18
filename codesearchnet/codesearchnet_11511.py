def register_chooser(self, chooser, **kwargs):
        """Adds a model chooser definition to the registry."""
        if not issubclass(chooser, Chooser):
            return self.register_simple_chooser(chooser, **kwargs)

        self.choosers[chooser.model] = chooser(**kwargs)
        return chooser