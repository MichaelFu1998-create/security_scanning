def move_dot(self):
        """Returns the DottedRule that results from moving the dot."""
        return self.__class__(self.production, self.pos + 1, self.lookahead)