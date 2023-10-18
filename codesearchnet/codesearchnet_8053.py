def geo(lat, lon, radius, unit='km'):
    """
    Indicate that value is a geo region
    """
    return GeoValue(lat, lon, radius, unit)