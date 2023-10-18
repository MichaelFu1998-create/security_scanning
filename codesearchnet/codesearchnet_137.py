def clip_out_of_image(self):
        """
        Clip off all parts from all bounding boxes that are outside of the image.

        Returns
        -------
        imgaug.BoundingBoxesOnImage
            Bounding boxes, clipped to fall within the image dimensions.

        """
        bbs_cut = [bb.clip_out_of_image(self.shape)
                   for bb in self.bounding_boxes if bb.is_partly_within_image(self.shape)]
        return BoundingBoxesOnImage(bbs_cut, shape=self.shape)