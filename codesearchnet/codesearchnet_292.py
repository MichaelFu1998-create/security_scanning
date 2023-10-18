def to_bounding_box(self):
        """
        Generate a bounding box encapsulating the line string.

        Returns
        -------
        None or imgaug.augmentables.bbs.BoundingBox
            Bounding box encapsulating the line string.
            ``None`` if the line string contained no points.

        """
        from .bbs import BoundingBox
        # we don't have to mind the case of len(.) == 1 here, because
        # zero-sized BBs are considered valid
        if len(self.coords) == 0:
            return None
        return BoundingBox(x1=np.min(self.xx), y1=np.min(self.yy),
                           x2=np.max(self.xx), y2=np.max(self.yy),
                           label=self.label)