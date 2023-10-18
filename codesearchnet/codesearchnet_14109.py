def color(self, d=0.035):
        """
        Returns a random color within the theme.

        Fetches a random range (the weight is taken into account,
        so ranges with a bigger weight have a higher chance of propagating)
        and hues it with the associated color.
        """
        s = sum([w for clr, rng, w in self.ranges])
        r = random()
        for clr, rng, weight in self.ranges:
            if weight / s >= r: break
            r -= weight / s

        return rng(clr, d)