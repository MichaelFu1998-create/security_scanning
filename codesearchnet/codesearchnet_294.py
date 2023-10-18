def to_heatmap(self, image_shape, size_lines=1, size_points=0,
                   antialiased=True, raise_if_out_of_image=False):
        """
        Generate a heatmap object from the line string.

        This is similar to
        :func:`imgaug.augmentables.lines.LineString.draw_lines_heatmap_array`
        executed with ``alpha=1.0``. The result is wrapped in a
        ``HeatmapsOnImage`` object instead of just an array.
        No points are drawn.

        Parameters
        ----------
        image_shape : tuple of int
            The shape of the image onto which to draw the line mask.

        size_lines : int, optional
            Thickness of the line.

        size_points : int, optional
            Size of the points in pixels.

        antialiased : bool, optional
            Whether to draw the line with anti-aliasing activated.

        raise_if_out_of_image : bool, optional
            Whether to raise an error if the line string is fully
            outside of the image. If set to False, no error will be raised and
            only the parts inside the image will be drawn.

        Returns
        -------
        imgaug.augmentables.heatmaps.HeatmapOnImage
            Heatmap object containing drawn line string.

        """
        from .heatmaps import HeatmapsOnImage
        return HeatmapsOnImage(
            self.draw_heatmap_array(
                image_shape, size_lines=size_lines, size_points=size_points,
                antialiased=antialiased,
                raise_if_out_of_image=raise_if_out_of_image),
            shape=image_shape
        )