def union(self, other):
        """
        Compute the union bounding box of this bounding box and another one.

        This is equivalent to drawing a bounding box around all corners points of both
        bounding boxes.

        Parameters
        ----------
        other : imgaug.BoundingBox
            Other bounding box with which to generate the union.

        Returns
        -------
        imgaug.BoundingBox
            Union bounding box of the two bounding boxes.

        """
        return BoundingBox(
            x1=min(self.x1, other.x1),
            y1=min(self.y1, other.y1),
            x2=max(self.x2, other.x2),
            y2=max(self.y2, other.y2),
        )