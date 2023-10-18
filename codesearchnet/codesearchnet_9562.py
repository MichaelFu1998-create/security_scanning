def bounds_at_zoom(self, zoom=None):
        """
        Return process bounds for zoom level.

        Parameters
        ----------
        zoom : integer or list

        Returns
        -------
        process bounds : tuple
            left, bottom, right, top
        """
        return () if self.area_at_zoom(zoom).is_empty else Bounds(
            *self.area_at_zoom(zoom).bounds)