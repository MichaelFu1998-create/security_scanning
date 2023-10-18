def _weight_by_hue(self):
        """
        Returns a list of (hue, ranges, total weight, normalized total weight)-tuples.

        ColorTheme is made up out of (color, range, weight) tuples.
        For consistency with XML-output in the old Prism format
        (i.e. <color>s made up of <shade>s) we need a group
        weight per different hue.

        The same is true for the swatch() draw method.
        Hues are grouped as a single unit (e.g. dark red, intense red, weak red)
        after which the dimensions (rows/columns) is determined.
        """
        grouped = {}
        weights = []
        for clr, rng, weight in self.ranges:
            h = clr.nearest_hue(primary=False)
            if grouped.has_key(h):
                ranges, total_weight = grouped[h]
                ranges.append((clr, rng, weight))
                total_weight += weight
                grouped[h] = (ranges, total_weight)
            else:
                grouped[h] = ([(clr, rng, weight)], weight)

        # Calculate the normalized (0.0-1.0) weight for each hue,
        # and transform the dictionary to a list.
        s = 1.0 * sum([w for r, w in grouped.values()])
        grouped = [(grouped[h][1], grouped[h][1] / s, h, grouped[h][0]) for h in grouped]
        grouped.sort()
        grouped.reverse()

        return grouped