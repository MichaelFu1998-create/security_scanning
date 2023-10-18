def reproject_geometry(
    geometry, src_crs=None, dst_crs=None, error_on_clip=False, validity_check=True,
    antimeridian_cutting=False
):
    """
    Reproject a geometry to target CRS.

    Also, clips geometry if it lies outside the destination CRS boundary.
    Supported destination CRSes for clipping: 4326 (WGS84), 3857 (Spherical
    Mercator) and 3035 (ETRS89 / ETRS-LAEA).

    Parameters
    ----------
    geometry : ``shapely.geometry``
    src_crs : ``rasterio.crs.CRS`` or EPSG code
        CRS of source data
    dst_crs : ``rasterio.crs.CRS`` or EPSG code
        target CRS
    error_on_clip : bool
        raises a ``RuntimeError`` if a geometry is outside of CRS bounds
        (default: False)
    validity_check : bool
        checks if reprojected geometry is valid and throws ``TopologicalError``
        if invalid (default: True)
    antimeridian_cutting : bool
        cut geometry at Antimeridian; can result in a multipart output geometry

    Returns
    -------
    geometry : ``shapely.geometry``
    """
    src_crs = _validated_crs(src_crs)
    dst_crs = _validated_crs(dst_crs)

    def _reproject_geom(geometry, src_crs, dst_crs):
        if geometry.is_empty:
            return geometry
        else:
            out_geom = to_shape(
                transform_geom(
                    src_crs.to_dict(),
                    dst_crs.to_dict(),
                    mapping(geometry),
                    antimeridian_cutting=antimeridian_cutting
                )
            )
            return _repair(out_geom) if validity_check else out_geom

    # return repaired geometry if no reprojection needed
    if src_crs == dst_crs or geometry.is_empty:
        return _repair(geometry)

    # geometry needs to be clipped to its CRS bounds
    elif (
        dst_crs.is_epsg_code and               # just in case for an CRS with EPSG code
        dst_crs.get("init") in CRS_BOUNDS and  # if CRS has defined bounds
        dst_crs.get("init") != "epsg:4326"     # and is not WGS84 (does not need clipping)
    ):
        wgs84_crs = CRS().from_epsg(4326)
        # get dst_crs boundaries
        crs_bbox = box(*CRS_BOUNDS[dst_crs.get("init")])
        # reproject geometry to WGS84
        geometry_4326 = _reproject_geom(geometry, src_crs, wgs84_crs)
        # raise error if geometry has to be clipped
        if error_on_clip and not geometry_4326.within(crs_bbox):
            raise RuntimeError("geometry outside target CRS bounds")
        # clip geometry dst_crs boundaries and return
        return _reproject_geom(crs_bbox.intersection(geometry_4326), wgs84_crs, dst_crs)

    # return without clipping if destination CRS does not have defined bounds
    else:
        return _reproject_geom(geometry, src_crs, dst_crs)