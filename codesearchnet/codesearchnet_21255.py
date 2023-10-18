def relative_to(self, other):
        """
        Important here is, that both are always the same:
        both with \\?\ prefix or both without it.
        """
        return super(WindowsPath2, Path2(self.path)).relative_to(Path2(other).path)