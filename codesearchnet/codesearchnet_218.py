def to_bounding_box(self):
        """
        Convert this polygon to a bounding box tightly containing the whole polygon.

        Returns
        -------
        imgaug.BoundingBox
            Tight bounding box around the polygon.

        """
        # TODO get rid of this deferred import
        from imgaug.augmentables.bbs import BoundingBox

        xx = self.xx
        yy = self.yy
        return BoundingBox(x1=min(xx), x2=max(xx), y1=min(yy), y2=max(yy), label=self.label)