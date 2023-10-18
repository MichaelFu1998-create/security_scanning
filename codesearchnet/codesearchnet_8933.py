def search_for_comment(self, lineno, default=None):
        """ Find the comment block just before the given line number.

        Returns None (or the specified default) if there is no such block.
        """
        if not self.index:
            self.make_index()
        block = self.index.get(lineno, None)
        text = getattr(block, 'text', default)
        return text