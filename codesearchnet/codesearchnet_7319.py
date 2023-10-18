def _add_active_assets(specs):
    """
    This function adds an assets key to the specs, which is filled in with a dictionary
    of all assets defined by apps and libs in the specs
    """
    specs['assets'] = {}
    for spec in specs.get_apps_and_libs():
        for asset in spec['assets']:
            if not specs['assets'].get(asset['name']):
                specs['assets'][asset['name']] = {}
                specs['assets'][asset['name']]['required_by'] = set()
                specs['assets'][asset['name']]['used_by'] = set()
            specs['assets'][asset['name']]['used_by'].add(spec.name)
            if asset['required']:
                specs['assets'][asset['name']]['required_by'].add(spec.name)