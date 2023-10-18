def extend(self, all_sides=0, top=0, right=0, bottom=0, left=0):
        """
        Extend the size of the bounding box along its sides.

        Parameters
        ----------
        all_sides : number, optional
            Value by which to extend the bounding box size along all sides.

        top : number, optional
            Value by which to extend the bounding box size along its top side.

        right : number, optional
            Value by which to extend the bounding box size along its right side.

        bottom : number, optional
            Value by which to extend the bounding box size along its bottom side.

        left : number, optional
            Value by which to extend the bounding box size along its left side.

        Returns
        -------
        imgaug.BoundingBox
            Extended bounding box.

        """
        return BoundingBox(
            x1=self.x1 - all_sides - left,
            x2=self.x2 + all_sides + right,
            y1=self.y1 - all_sides - top,
            y2=self.y2 + all_sides + bottom
        )