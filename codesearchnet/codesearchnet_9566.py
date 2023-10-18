def profile(self):
        """Return raster metadata."""
        with rasterio.open(self.path, "r") as src:
            return deepcopy(src.meta)