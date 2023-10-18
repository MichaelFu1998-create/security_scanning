def remove_out_of_image(self, fully=True, partly=False):
        """
        Remove all bounding boxes that are fully or partially outside of the image.

        Parameters
        ----------
        fully : bool, optional
            Whether to remove bounding boxes that are fully outside of the image.

        partly : bool, optional
            Whether to remove bounding boxes that are partially outside of the image.

        Returns
        -------
        imgaug.BoundingBoxesOnImage
            Reduced set of bounding boxes, with those that were fully/partially outside of
            the image removed.

        """
        bbs_clean = [bb for bb in self.bounding_boxes
                     if not bb.is_out_of_image(self.shape, fully=fully, partly=partly)]
        return BoundingBoxesOnImage(bbs_clean, shape=self.shape)