def get(self, name):
        """ Return component by category name """
        for c in self.comps:
            if c.category == name:
                return c
        return None