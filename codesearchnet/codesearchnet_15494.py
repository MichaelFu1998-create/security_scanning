def blocks(self, name):
        """
        Search for defined blocks recursively.
        Allow '>' to be ignored. '.a .b' == '.a > .b'
        Args:
            name (string): Search term
        Returns:
            Block object OR False
        """
        b = self._blocks(name)
        if b:
            return b
        return self._blocks(name.replace('?>?', ' '))