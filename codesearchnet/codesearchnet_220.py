def to_line_string(self, closed=True):
        """
        Convert this polygon's `exterior` to a ``LineString`` instance.

        Parameters
        ----------
        closed : bool, optional
            Whether to close the line string, i.e. to add the first point of
            the `exterior` also as the last point at the end of the line string.
            This has no effect if the polygon has a single point or zero
            points.

        Returns
        -------
        imgaug.augmentables.lines.LineString
            Exterior of the polygon as a line string.

        """
        from imgaug.augmentables.lines import LineString
        if not closed or len(self.exterior) <= 1:
            return LineString(self.exterior, label=self.label)
        return LineString(
            np.concatenate([self.exterior, self.exterior[0:1, :]], axis=0),
            label=self.label)