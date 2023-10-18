def recombine(self, other, d=0.7):
        """
        Genetic recombination of two themes using cut and splice technique.
        """
        a, b = self, other
        d1 = max(0, min(d, 1))
        d2 = d1

        c = ColorTheme(
            name=a.name[:int(len(a.name) * d1)] +
                 b.name[int(len(b.name) * d2):],
            ranges=a.ranges[:int(len(a.ranges) * d1)] +
                   b.ranges[int(len(b.ranges) * d2):],
            top=a.top,
            cache=os.path.join(DEFAULT_CACHE, "recombined"),
            blue=a.blue,
            length=a.length * d1 + b.length * d2
        )
        c.tags = a.tags[:int(len(a.tags) * d1)]
        c.tags += b.tags[int(len(b.tags) * d2):]
        return c