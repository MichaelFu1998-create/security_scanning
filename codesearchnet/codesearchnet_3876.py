def register(self, type):
        """
        Registers a custom formatting function with ub.repr2
        """
        def _decorator(func):
            if isinstance(type, tuple):
                for t in type:
                    self.func_registry[t] = func
            else:
                self.func_registry[type] = func
            return func
        return _decorator