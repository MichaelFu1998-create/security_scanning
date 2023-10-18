def resource_basename(resource):
    """Last component of a resource (which always uses '/' as sep)."""
    if resource.endswith('/'):
         resource = resource[:-1]
    parts = resource.split('/')
    return parts[-1]