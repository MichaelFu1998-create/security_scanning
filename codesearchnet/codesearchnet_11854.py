def get_thumbprint(self):
        """
        Calculates the current thumbprint of the item being tracked.
        """
        d = {}
        settings = dj.get_settings()
        for name in self.names:
            d[name] = getattr(settings, name)
        return d