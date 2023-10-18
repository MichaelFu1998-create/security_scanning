def intersection(self, other, default=None):
        """
        Compute the intersection bounding box of this bounding box and another one.

        Note that in extreme cases, the intersection can be a single point, meaning that the intersection bounding box
        will exist, but then also has a height and width of zero.

        Parameters
        ----------
        other : imgaug.BoundingBox
            Other bounding box with which to generate the intersection.

        default : any, optional
            Default value to return if there is no intersection.

        Returns
        -------
        imgaug.BoundingBox or any
            Intersection bounding box of the two bounding boxes if there is an intersection.
            If there is no intersection, the default value will be returned, which can by anything.

        """
        x1_i = max(self.x1, other.x1)
        y1_i = max(self.y1, other.y1)
        x2_i = min(self.x2, other.x2)
        y2_i = min(self.y2, other.y2)
        if x1_i > x2_i or y1_i > y2_i:
            return default
        else:
            return BoundingBox(x1=x1_i, y1=y1_i, x2=x2_i, y2=y2_i)