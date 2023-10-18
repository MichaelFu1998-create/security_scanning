def write(self, process_tile, data):
        """
        Write data from process tiles into GeoJSON file(s).

        Parameters
        ----------
        process_tile : ``BufferedTile``
            must be member of process ``TilePyramid``
        """
        if data is None or len(data) == 0:
            return
        if not isinstance(data, (list, types.GeneratorType)):
            raise TypeError(
                "GeoJSON driver data has to be a list or generator of GeoJSON objects"
            )

        data = list(data)

        if not len(data):
            logger.debug("no features to write")
        else:
            # in case of S3 output, create an boto3 resource
            bucket_resource = get_boto3_bucket(self._bucket) if self._bucket else None

            # Convert from process_tile to output_tiles
            for tile in self.pyramid.intersecting(process_tile):
                out_path = self.get_path(tile)
                self.prepare_path(tile)
                out_tile = BufferedTile(tile, self.pixelbuffer)
                write_vector_window(
                    in_data=data,
                    out_schema=self.output_params["schema"],
                    out_tile=out_tile,
                    out_path=out_path,
                    bucket_resource=bucket_resource
                )