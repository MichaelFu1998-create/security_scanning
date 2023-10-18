def variables(self, name):
        """Search for variable by name. Searches scope top down
        Args:
            name (string): Search term
        Returns:
            Variable object OR False
        """
        if isinstance(name, tuple):
            name = name[0]
        if name.startswith('@{'):
            name = '@' + name[2:-1]
        i = len(self)
        while i >= 0:
            i -= 1
            if name in self[i]['__variables__']:
                return self[i]['__variables__'][name]
        return False