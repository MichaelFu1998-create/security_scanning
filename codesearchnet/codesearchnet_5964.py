def get_cache_access_details(key=None):
    """Retrieve detailed cache information."""
    from cloudaux.gcp.decorators import _GCP_CACHE
    return _GCP_CACHE.get_access_details(key=key)