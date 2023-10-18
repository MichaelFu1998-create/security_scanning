def _get_referenced_services(specs):
    """
    Returns all services that are referenced in specs.apps.depends.services,
    or in specs.bundles.services
    """
    active_services = set()
    for app_spec in specs['apps'].values():
        for service in app_spec['depends']['services']:
            active_services.add(service)
    for bundle_spec in specs['bundles'].values():
        for service in bundle_spec['services']:
            active_services.add(service)
    return active_services