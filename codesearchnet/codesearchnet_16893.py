def _kwargs(self):
        """Keyword arguments for recreating the Shape from the vertices.

        """
        return dict(color=self.color, velocity=self.velocity, colors=self.colors)