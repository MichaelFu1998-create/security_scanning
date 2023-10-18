def pxbounds(self, geom, clip=False):
        """ Returns the bounds of a geometry object in pixel coordinates

        Args:
            geom: Shapely geometry object or GeoJSON as Python dictionary or WKT string
            clip (bool): Clip the bounds to the min/max extent of the image

        Returns:
            list: bounds in pixels [min x, min y, max x, max y] clipped to image bounds
        """

        try:
            if isinstance(geom, dict):
                if 'geometry' in geom:
                    geom = shape(geom['geometry'])
                else:
                    geom = shape(geom)
            elif isinstance(geom, BaseGeometry):
                geom = shape(geom)
            else:
                geom = wkt.loads(geom)
        except:
            raise TypeError ("Invalid geometry object")

        # if geometry doesn't overlap the image, return an error
        if geom.disjoint(shape(self)):
            raise ValueError("Geometry outside of image bounds")
        # clip to pixels within the image
        (xmin, ymin, xmax, ymax) = ops.transform(self.__geo_transform__.rev, geom).bounds
        _nbands, ysize, xsize = self.shape
        if clip:
            xmin = max(xmin, 0)
            ymin = max(ymin, 0)
            xmax = min(xmax, xsize)
            ymax = min(ymax, ysize)

        return (xmin, ymin, xmax, ymax)