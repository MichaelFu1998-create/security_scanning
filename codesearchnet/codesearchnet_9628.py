def resample_from_array(
    in_raster=None,
    in_affine=None,
    out_tile=None,
    in_crs=None,
    resampling="nearest",
    nodataval=0
):
    """
    Extract and resample from array to target tile.

    Parameters
    ----------
    in_raster : array
    in_affine : ``Affine``
    out_tile : ``BufferedTile``
    resampling : string
        one of rasterio's resampling methods (default: nearest)
    nodataval : integer or float
        raster nodata value (default: 0)

    Returns
    -------
    resampled array : array
    """
    # TODO rename function
    if isinstance(in_raster, ma.MaskedArray):
        pass
    if isinstance(in_raster, np.ndarray):
        in_raster = ma.MaskedArray(in_raster, mask=in_raster == nodataval)
    elif isinstance(in_raster, ReferencedRaster):
        in_affine = in_raster.affine
        in_crs = in_raster.crs
        in_raster = in_raster.data
    elif isinstance(in_raster, tuple):
        in_raster = ma.MaskedArray(
            data=np.stack(in_raster),
            mask=np.stack([
                band.mask
                if isinstance(band, ma.masked_array)
                else np.where(band == nodataval, True, False)
                for band in in_raster
            ]),
            fill_value=nodataval
        )
    else:
        raise TypeError("wrong input data type: %s" % type(in_raster))
    if in_raster.ndim == 2:
        in_raster = ma.expand_dims(in_raster, axis=0)
    elif in_raster.ndim == 3:
        pass
    else:
        raise TypeError("input array must have 2 or 3 dimensions")
    if in_raster.fill_value != nodataval:
        ma.set_fill_value(in_raster, nodataval)
    out_shape = (in_raster.shape[0], ) + out_tile.shape
    dst_data = np.empty(out_shape, in_raster.dtype)
    in_raster = ma.masked_array(
        data=in_raster.filled(), mask=in_raster.mask, fill_value=nodataval
    )
    reproject(
        in_raster,
        dst_data,
        src_transform=in_affine,
        src_crs=in_crs if in_crs else out_tile.crs,
        dst_transform=out_tile.affine,
        dst_crs=out_tile.crs,
        resampling=Resampling[resampling]
    )
    return ma.MaskedArray(dst_data, mask=dst_data == nodataval)