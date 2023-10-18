def time_zone_by_country_and_region(country_code, region_code=None):
    """
    Returns time zone from country and region code.

    :arg country_code: Country code
    :arg region_code: Region code
    """
    timezone = country_dict.get(country_code)
    if not timezone:
        return None

    if isinstance(timezone, str):
        return timezone

    return timezone.get(region_code)