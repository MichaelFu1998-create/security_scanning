def warp(self, dem=None, proj="EPSG:4326", **kwargs):
        """Delayed warp across an entire AOI or Image

        Creates a new dask image by deferring calls to the warp_geometry on chunks

        Args:
            dem (ndarray): optional. A DEM for warping to specific elevation planes
            proj (str): optional. An EPSG proj string to project the image data into ("EPSG:32612")

        Returns:
            daskarray: a warped image as deferred image array
        """
        try:
            img_md = self.rda.metadata["image"]
            x_size = img_md["tileXSize"]
            y_size = img_md["tileYSize"]
        except (AttributeError, KeyError):
            x_size = kwargs.get("chunk_size", 256)
            y_size = kwargs.get("chunk_size", 256)

        # Create an affine transform to convert between real-world and pixels
        if self.proj is None:
            from_proj = "EPSG:4326"
        else:
            from_proj = self.proj

        try:
            # NOTE: this only works on images that have rda rpcs metadata
            center = wkt.loads(self.rda.metadata["image"]["imageBoundsWGS84"]).centroid
            g = box(*(center.buffer(self.rda.metadata["rpcs"]["gsd"] / 2).bounds))
            tfm = partial(pyproj.transform, pyproj.Proj(init="EPSG:4326"), pyproj.Proj(init=proj))
            gsd = kwargs.get("gsd", ops.transform(tfm, g).area ** 0.5)
            current_bounds = wkt.loads(self.rda.metadata["image"]["imageBoundsWGS84"]).bounds
        except (AttributeError, KeyError, TypeError):
            tfm = partial(pyproj.transform, pyproj.Proj(init=self.proj), pyproj.Proj(init=proj))
            gsd = kwargs.get("gsd", (ops.transform(tfm, shape(self)).area / (self.shape[1] * self.shape[2])) ** 0.5 )
            current_bounds = self.bounds

        tfm = partial(pyproj.transform, pyproj.Proj(init=from_proj), pyproj.Proj(init=proj))
        itfm = partial(pyproj.transform, pyproj.Proj(init=proj), pyproj.Proj(init=from_proj))
        output_bounds = ops.transform(tfm, box(*current_bounds)).bounds
        gtf = Affine.from_gdal(output_bounds[0], gsd, 0.0, output_bounds[3], 0.0, -1 * gsd)

        ll = ~gtf * (output_bounds[:2])
        ur = ~gtf * (output_bounds[2:])
        x_chunks = int((ur[0] - ll[0]) / x_size) + 1
        y_chunks = int((ll[1] - ur[1]) / y_size) + 1

        num_bands = self.shape[0]

        try:
            dtype = RDA_TO_DTYPE[img_md["dataType"]]
        except:
            dtype = 'uint8'

        daskmeta = {
            "dask": {},
            "chunks": (num_bands, y_size, x_size),
            "dtype": dtype,
            "name": "warp-{}".format(self.name),
            "shape": (num_bands, y_chunks * y_size, x_chunks * x_size)
        }

        def px_to_geom(xmin, ymin):
            xmax = int(xmin + x_size)
            ymax = int(ymin + y_size)
            bounds = list((gtf * (xmin, ymax)) + (gtf * (xmax, ymin)))
            return box(*bounds)

        full_bounds = box(*output_bounds)

        dasks = []
        if isinstance(dem, GeoDaskImage):
            if dem.proj != proj:
                dem = dem.warp(proj=proj, dem=dem)
            dasks.append(dem.dask)

        for y in xrange(y_chunks):
            for x in xrange(x_chunks):
                xmin = x * x_size
                ymin = y * y_size
                geometry = px_to_geom(xmin, ymin)
                daskmeta["dask"][(daskmeta["name"], 0, y, x)] = (self._warp, geometry, gsd, dem, proj, dtype, 5)
        daskmeta["dask"], _ = optimization.cull(HighLevelGraph.merge(daskmeta["dask"], *dasks), list(daskmeta["dask"].keys()))

        gi = mapping(full_bounds)
        gt = AffineTransform(gtf, proj)
        image = GeoDaskImage(daskmeta, __geo_interface__ = gi, __geo_transform__ = gt)
        return image[box(*output_bounds)]