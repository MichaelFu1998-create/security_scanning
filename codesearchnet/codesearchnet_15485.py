def raw(self, clean=False):
        """Raw identifier.
        args:
            clean (bool): clean name
        returns:
            str
        """
        if clean:
            return ''.join(''.join(p) for p in self.parsed).replace('?', ' ')
        return '%'.join('%'.join(p) for p in self.parsed).strip().strip('%')