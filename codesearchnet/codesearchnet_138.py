def shift(self, top=None, right=None, bottom=None, left=None):
        """
        Shift all bounding boxes from one or more image sides, i.e. move them on the x/y-axis.

        Parameters
        ----------
        top : None or int, optional
            Amount of pixels by which to shift all bounding boxes from the top.

        right : None or int, optional
            Amount of pixels by which to shift all bounding boxes from the right.

        bottom : None or int, optional
            Amount of pixels by which to shift all bounding boxes from the bottom.

        left : None or int, optional
            Amount of pixels by which to shift all bounding boxes from the left.

        Returns
        -------
        imgaug.BoundingBoxesOnImage
            Shifted bounding boxes.

        """
        bbs_new = [bb.shift(top=top, right=right, bottom=bottom, left=left) for bb in self.bounding_boxes]
        return BoundingBoxesOnImage(bbs_new, shape=self.shape)