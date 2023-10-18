def lookup(self, data):
        """
        Returns an appropriate function to format `data` if one has been
        registered.
        """
        for func in self.lazy_init:
            func()

        for type, func in self.func_registry.items():
            if isinstance(data, type):
                return func