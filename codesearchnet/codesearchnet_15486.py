def copy(self):
        """ Return copy of self
        Returns:
            Identifier object
        """
        tokens = ([t for t in self.tokens]
                  if isinstance(self.tokens, list) else self.tokens)
        return Identifier(tokens, 0)