def get_centroid_of_stops(gtfs):
    """
    Get mean latitude AND longitude of stops

    Parameters
    ----------
    gtfs: GTFS

    Returns
    -------
    mean_lat : float
    mean_lon : float
    """
    stops = gtfs.get_table("stops")
    mean_lat = numpy.mean(stops['lat'].values)
    mean_lon = numpy.mean(stops['lon'].values)
    return mean_lat, mean_lon