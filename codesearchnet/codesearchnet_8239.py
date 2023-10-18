def detach(self, overlay):
        """
        Give each animation a unique, mutable layout so they can run
        independently.
        """
        # See #868
        for i, a in enumerate(self.animations):
            a.layout = a.layout.clone()
            if overlay and i:
                a.preclear = False