def deepcopy(self):
        """
        Create a deep copy of the PolygonsOnImage object.

        Returns
        -------
        imgaug.PolygonsOnImage
            Deep copy.

        """
        # Manual copy is far faster than deepcopy for PolygonsOnImage,
        # so use manual copy here too
        polys = [poly.deepcopy() for poly in self.polygons]
        return PolygonsOnImage(polys, tuple(self.shape))