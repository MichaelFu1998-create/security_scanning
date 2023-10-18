def get_median_lat_lon_of_stops(gtfs):
    """
    Get median latitude AND longitude of stops

    Parameters
    ----------
    gtfs: GTFS

    Returns
    -------
    median_lat : float
    median_lon : float
    """
    stops = gtfs.get_table("stops")
    median_lat = numpy.percentile(stops['lat'].values, 50)
    median_lon = numpy.percentile(stops['lon'].values, 50)
    return median_lat, median_lon