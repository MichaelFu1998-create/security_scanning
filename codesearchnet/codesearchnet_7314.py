def _get_referenced_apps(specs):
    """
    Returns a set of all apps that are required to run any bundle in specs[constants.CONFIG_BUNDLES_KEY]
    """
    activated_bundles = specs[constants.CONFIG_BUNDLES_KEY].keys()
    all_active_apps = set()
    for active_bundle in activated_bundles:
        bundle_spec = specs[constants.CONFIG_BUNDLES_KEY].get(active_bundle)
        for app_name in bundle_spec['apps']:
            all_active_apps.add(app_name)
            all_active_apps |= _get_dependent('apps', app_name, specs, 'apps')
    return all_active_apps