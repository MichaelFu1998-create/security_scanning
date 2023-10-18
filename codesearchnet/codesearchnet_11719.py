def get_thumbprint(self):
        """
        Calculates the current thumbprint of the item being tracked.
        """
        d = {}
        if self.names:
            names = self.names
        else:
            names = list(self.satchel.lenv)
        for name in self.names:
            d[name] = deepcopy(self.satchel.env[name])
        return d