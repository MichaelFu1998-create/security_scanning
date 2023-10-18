def _expand_spatial_bounds_to_fit_axes(bounds, ax_width, ax_height):
    """
    Parameters
    ----------
    bounds: dict
    ax_width: float
    ax_height: float

    Returns
    -------
    spatial_bounds
    """
    b = bounds
    height_meters = util.wgs84_distance(b['lat_min'], b['lon_min'], b['lat_max'], b['lon_min'])
    width_meters = util.wgs84_distance(b['lat_min'], b['lon_min'], b['lat_min'], b['lon_max'])
    x_per_y_meters = width_meters / height_meters
    x_per_y_axes = ax_width / ax_height
    if x_per_y_axes > x_per_y_meters:  # x-axis
        # axis x_axis has slack -> the spatial longitude bounds need to be extended
        width_meters_new = (height_meters * x_per_y_axes)
        d_lon_new = ((b['lon_max'] - b['lon_min']) / width_meters) * width_meters_new
        mean_lon = (b['lon_min'] + b['lon_max'])/2.
        lon_min = mean_lon - d_lon_new / 2.
        lon_max = mean_lon + d_lon_new / 2.
        spatial_bounds = {
            "lon_min": lon_min,
            "lon_max": lon_max,
            "lat_min": b['lat_min'],
            "lat_max": b['lat_max']
        }
    else:
        # axis y_axis has slack -> the spatial latitude bounds need to be extended
        height_meters_new = (width_meters / x_per_y_axes)
        d_lat_new = ((b['lat_max'] - b['lat_min']) / height_meters) * height_meters_new
        mean_lat = (b['lat_min'] + b['lat_max']) / 2.
        lat_min = mean_lat - d_lat_new / 2.
        lat_max = mean_lat + d_lat_new / 2.
        spatial_bounds = {
            "lon_min": b['lon_min'],
            "lon_max": b['lon_max'],
            "lat_min": lat_min,
            "lat_max": lat_max
        }
    return spatial_bounds