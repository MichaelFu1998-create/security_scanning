def deepcopy(self):
        """
        Create a deep copy of the BoundingBoxesOnImage object.

        Returns
        -------
        imgaug.BoundingBoxesOnImage
            Deep copy.

        """
        # Manual copy is far faster than deepcopy for BoundingBoxesOnImage,
        # so use manual copy here too
        bbs = [bb.deepcopy() for bb in self.bounding_boxes]
        return BoundingBoxesOnImage(bbs, tuple(self.shape))