def swatch(self, x, y, w=35, h=35, padding=4, roundness=0, n=12, d=0.035, grouped=None):
        """
        Draws a weighted swatch with approximately n columns and rows.

        When the grouped parameter is True, colors are grouped in blocks of the same hue
        (also see the _weight_by_hue() method).
        """
        if grouped is None:  # should be True or False
            grouped = self.group_swatches

        # If we dont't need to make groups,
        # just display an individual column for each weight
        # in the (color, range, weight) tuples.
        if not grouped:
            s = sum([wgt for clr, rng, wgt in self.ranges])
            for clr, rng, wgt in self.ranges:
                cols = max(1, int(wgt / s * n))
                for i in _range(cols):
                    rng.colors(clr, n=n, d=d).swatch(x, y, w, h, padding=padding, roundness=roundness)
                    x += w + padding

            return x, y + n * (h + padding)

        # When grouped, combine hues and display them
        # in batches of rows, then moving on to the next hue.
        grouped = self._weight_by_hue()
        for total_weight, normalized_weight, hue, ranges in grouped:
            dy = y
            rc = 0
            for clr, rng, weight in ranges:
                dx = x
                cols = int(normalized_weight * n)
                cols = max(1, min(cols, n - len(grouped)))
                if clr.name == "black": rng = rng.black
                if clr.name == "white": rng = rng.white
                for i in _range(cols):
                    rows = int(weight / total_weight * n)
                    rows = max(1, rows)
                    # Each column should add up to n rows,
                    # if not due to rounding errors, add a row at the bottom.
                    if (clr, rng, weight) == ranges[-1] and rc + rows < n: rows += 1
                    rng.colors(clr, n=rows, d=d).swatch(dx, dy, w, h, padding=padding, roundness=roundness)
                    dx += w + padding
                dy += (w + padding) * rows  # + padding
                rc = rows
            x += (w + padding) * cols + padding

        return x, dy