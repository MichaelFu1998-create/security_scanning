def copy(self):

        """ Returns a deep copy of the list.
        """

        return ColorList(
            [color(clr.r, clr.g, clr.b, clr.a, mode="rgb") for clr in self],
            name=self.name,
            tags=self.tags
        )