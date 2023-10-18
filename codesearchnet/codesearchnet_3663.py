def _declare(self, var):
        """ Declare the variable `var` """
        if var.name in self._declarations:
            raise ValueError('Variable already declared')
        self._declarations[var.name] = var
        return var