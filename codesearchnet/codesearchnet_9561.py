def area_at_zoom(self, zoom=None):
        """
        Return process bounding box for zoom level.

        Parameters
        ----------
        zoom : int or None
            if None, the union of all zoom level areas is returned

        Returns
        -------
        process area : shapely geometry
        """
        if zoom is None:
            if not self._cache_full_process_area:
                logger.debug("calculate process area ...")
                self._cache_full_process_area = cascaded_union([
                    self._area_at_zoom(z) for z in self.init_zoom_levels]
                ).buffer(0)
            return self._cache_full_process_area
        else:
            if zoom not in self.init_zoom_levels:
                raise ValueError(
                    "zoom level not available with current configuration")
            return self._area_at_zoom(zoom)