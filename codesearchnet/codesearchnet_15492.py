def mixins(self, name):
        """ Search mixins for name.
        Allow '>' to be ignored. '.a .b()' == '.a > .b()'
        Args:
            name (string): Search term
        Returns:
            Mixin object list OR False
        """
        m = self._smixins(name)
        if m:
            return m
        return self._smixins(name.replace('?>?', ' '))