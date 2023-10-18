def gen_cumulative_distances(stops):
    """
    Add a 'd' key for distances to a stop/shape-sequence.

    This takes a shape-sequence or stop-sequence, and adds an extra
    'd' key that is cumulative, geographic distances between each
    point. This uses `wgs84_distance` from the util module.  The
    distances are in meters.  Distances are rounded to the nearest
    integer, because otherwise JSON size increases greatly.

    Parameters
    ----------
    stops: list
        elements are dicts with 'lat' and 'lon' keys
        and the function adds the 'd' key ('d' stands for distance)
        to the dictionaries
    """
    stops[0]['d'] = 0.0
    for i in range(1, len(stops)):
        stops[i]['d'] = stops[i-1]['d'] + wgs84_distance(
            stops[i-1]['lat'], stops[i-1]['lon'],
            stops[i]['lat'], stops[i]['lon'],
            )
    for stop in stops:
        stop['d'] = int(stop['d'])