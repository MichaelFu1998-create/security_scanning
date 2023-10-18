def to_normalized_batch(self):
        """Convert this unnormalized batch to an instance of Batch.

        As this method is intended to be called before augmentation, it
        assumes that none of the ``*_aug`` attributes is yet set.
        It will produce an AssertionError otherwise.

        The newly created Batch's ``*_unaug`` attributes will match the ones
        in this batch, just in normalized form.

        Returns
        -------
        imgaug.augmentables.batches.Batch
            The batch, with ``*_unaug`` attributes being normalized.

        """
        assert all([
            attr is None for attr_name, attr in self.__dict__.items()
            if attr_name.endswith("_aug")]), \
            "Expected UnnormalizedBatch to not contain any augmented data " \
            "before normalization, but at least one '*_aug' attribute was " \
            "already set."

        images_unaug = nlib.normalize_images(self.images_unaug)
        shapes = None
        if images_unaug is not None:
            shapes = [image.shape for image in images_unaug]

        return Batch(
            images=images_unaug,
            heatmaps=nlib.normalize_heatmaps(
                self.heatmaps_unaug, shapes),
            segmentation_maps=nlib.normalize_segmentation_maps(
                self.segmentation_maps_unaug, shapes),
            keypoints=nlib.normalize_keypoints(
                self.keypoints_unaug, shapes),
            bounding_boxes=nlib.normalize_bounding_boxes(
                self.bounding_boxes_unaug, shapes),
            polygons=nlib.normalize_polygons(
                self.polygons_unaug, shapes),
            line_strings=nlib.normalize_line_strings(
                self.line_strings_unaug, shapes),
            data=self.data
        )