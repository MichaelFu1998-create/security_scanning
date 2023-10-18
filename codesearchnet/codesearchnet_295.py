def to_segmentation_map(self, image_shape, size_lines=1, size_points=0,
                            raise_if_out_of_image=False):
        """
        Generate a segmentation map object from the line string.

        This is similar to
        :func:`imgaug.augmentables.lines.LineString.draw_mask`.
        The result is wrapped in a ``SegmentationMapOnImage`` object
        instead of just an array.

        Parameters
        ----------
        image_shape : tuple of int
            The shape of the image onto which to draw the line mask.

        size_lines : int, optional
            Thickness of the line.

        size_points : int, optional
            Size of the points in pixels.

        raise_if_out_of_image : bool, optional
            Whether to raise an error if the line string is fully
            outside of the image. If set to False, no error will be raised and
            only the parts inside the image will be drawn.

        Returns
        -------
        imgaug.augmentables.segmaps.SegmentationMapOnImage
            Segmentation map object containing drawn line string.

        """
        from .segmaps import SegmentationMapOnImage
        return SegmentationMapOnImage(
            self.draw_mask(
                image_shape, size_lines=size_lines, size_points=size_points,
                raise_if_out_of_image=raise_if_out_of_image),
            shape=image_shape
        )