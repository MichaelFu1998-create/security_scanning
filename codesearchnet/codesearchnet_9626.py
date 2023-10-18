def write_raster_window(
    in_tile=None, in_data=None, out_profile=None, out_tile=None, out_path=None,
    tags=None, bucket_resource=None
):
    """
    Write a window from a numpy array to an output file.

    Parameters
    ----------
    in_tile : ``BufferedTile``
        ``BufferedTile`` with a data attribute holding NumPy data
    in_data : array
    out_profile : dictionary
        metadata dictionary for rasterio
    out_tile : ``Tile``
        provides output boundaries; if None, in_tile is used
    out_path : string
        output path to write to
    tags : optional tags to be added to GeoTIFF file
    bucket_resource : boto3 bucket resource to write to in case of S3 output
    """
    if not isinstance(out_path, str):
        raise TypeError("out_path must be a string")
    logger.debug("write %s", out_path)
    if out_path == "memoryfile":
        raise DeprecationWarning(
            "Writing to memoryfile with write_raster_window() is deprecated. "
            "Please use RasterWindowMemoryFile."
        )
    out_tile = in_tile if out_tile is None else out_tile
    _validate_write_window_params(in_tile, out_tile, in_data, out_profile)

    # extract data
    window_data = extract_from_array(
        in_raster=in_data,
        in_affine=in_tile.affine,
        out_tile=out_tile
    ) if in_tile != out_tile else in_data

    # use transform instead of affine
    if "affine" in out_profile:
        out_profile["transform"] = out_profile.pop("affine")

    # write if there is any band with non-masked data
    if window_data.all() is not ma.masked:

        try:
            if out_path.startswith("s3://"):
                with RasterWindowMemoryFile(
                    in_tile=out_tile,
                    in_data=window_data,
                    out_profile=out_profile,
                    out_tile=out_tile,
                    tags=tags
                ) as memfile:
                    logger.debug((out_tile.id, "upload tile", out_path))
                    bucket_resource.put_object(
                        Key="/".join(out_path.split("/")[3:]),
                        Body=memfile
                    )
            else:
                with rasterio.open(out_path, 'w', **out_profile) as dst:
                    logger.debug((out_tile.id, "write tile", out_path))
                    dst.write(window_data.astype(out_profile["dtype"], copy=False))
                    _write_tags(dst, tags)
        except Exception as e:
            logger.exception("error while writing file %s: %s", out_path, e)
            raise
    else:
        logger.debug((out_tile.id, "array window empty", out_path))