def fill_from_augmented_normalized_batch(self, batch_aug_norm):
        """
        Fill this batch with (normalized) augmentation results.

        This method receives a (normalized) Batch instance, takes all
        ``*_aug`` attributes out if it and assigns them to this
        batch *in unnormalized form*. Hence, the datatypes of all ``*_aug``
        attributes will match the datatypes of the ``*_unaug`` attributes.

        Parameters
        ----------
        batch_aug_norm: imgaug.augmentables.batches.Batch
            Batch after normalization and augmentation.

        Returns
        -------
        imgaug.augmentables.batches.UnnormalizedBatch
            New UnnormalizedBatch instance. All ``*_unaug`` attributes are
            taken from the old UnnormalizedBatch (without deepcopying them)
            and all ``*_aug`` attributes are taken from `batch_normalized`
            converted to unnormalized form.

        """
        # we take here the .data from the normalized batch instead of from
        # self for the rare case where one has decided to somehow change it
        # during augmentation
        batch = UnnormalizedBatch(
            images=self.images_unaug,
            heatmaps=self.heatmaps_unaug,
            segmentation_maps=self.segmentation_maps_unaug,
            keypoints=self.keypoints_unaug,
            bounding_boxes=self.bounding_boxes_unaug,
            polygons=self.polygons_unaug,
            line_strings=self.line_strings_unaug,
            data=batch_aug_norm.data
        )

        batch.images_aug = nlib.invert_normalize_images(
            batch_aug_norm.images_aug, self.images_unaug)
        batch.heatmaps_aug = nlib.invert_normalize_heatmaps(
            batch_aug_norm.heatmaps_aug, self.heatmaps_unaug)
        batch.segmentation_maps_aug = nlib.invert_normalize_segmentation_maps(
            batch_aug_norm.segmentation_maps_aug, self.segmentation_maps_unaug)
        batch.keypoints_aug = nlib.invert_normalize_keypoints(
            batch_aug_norm.keypoints_aug, self.keypoints_unaug)
        batch.bounding_boxes_aug = nlib.invert_normalize_bounding_boxes(
            batch_aug_norm.bounding_boxes_aug, self.bounding_boxes_unaug)
        batch.polygons_aug = nlib.invert_normalize_polygons(
            batch_aug_norm.polygons_aug, self.polygons_unaug)
        batch.line_strings_aug = nlib.invert_normalize_line_strings(
            batch_aug_norm.line_strings_aug, self.line_strings_unaug)

        return batch