def read_raster_no_crs(input_file, indexes=None, gdal_opts=None):
    """
    Wrapper function around rasterio.open().read().

    Parameters
    ----------
    input_file : str
        Path to file
    indexes : int or list
        Band index or list of band indexes to be read.

    Returns
    -------
    MaskedArray

    Raises
    ------
    FileNotFoundError if file cannot be found.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            with rasterio.Env(
                **get_gdal_options(
                    gdal_opts, is_remote=path_is_remote(input_file, s3=True)
                )
            ):
                with rasterio.open(input_file, "r") as src:
                    return src.read(indexes=indexes, masked=True)
        except RasterioIOError as e:
            for i in ("does not exist in the file system", "No such file or directory"):
                if i in str(e):
                    raise FileNotFoundError("%s not found" % input_file)
            else:
                raise