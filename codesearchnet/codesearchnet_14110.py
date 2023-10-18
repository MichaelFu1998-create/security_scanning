def colors(self, n=10, d=0.035):
        """
        Returns a number of random colors from the theme.
        """
        s = sum([w for clr, rng, w in self.ranges])
        colors = colorlist()
        for i in _range(n):
            r = random()
            for clr, rng, weight in self.ranges:
                if weight / s >= r: break
                r -= weight / s
            colors.append(rng(clr, d))

        return colors