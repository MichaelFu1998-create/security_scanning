def isValidClass(self, class_):
        """
        Needs to be its own method so it can be called from both wantClass and
        registerGoodClass.
        """
        module = inspect.getmodule(class_)
        valid = (
            module in self._valid_modules
            or (
                hasattr(module, '__file__')
                and module.__file__ in self._valid_named_modules
            )
        )
        return valid and not private(class_)