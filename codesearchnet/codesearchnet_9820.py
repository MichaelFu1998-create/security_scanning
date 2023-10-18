def get_spatial_bounds(gtfs, as_dict=False):
    """
    Parameters
    ----------
    gtfs

    Returns
    -------
    min_lon: float
    max_lon: float
    min_lat: float
    max_lat: float
    """
    stats = get_stats(gtfs)
    lon_min = stats['lon_min']
    lon_max = stats['lon_max']
    lat_min = stats['lat_min']
    lat_max = stats['lat_max']
    if as_dict:
        return {'lon_min': lon_min, 'lon_max': lon_max, 'lat_min': lat_min, 'lat_max': lat_max}
    else:
        return lon_min, lon_max, lat_min, lat_max