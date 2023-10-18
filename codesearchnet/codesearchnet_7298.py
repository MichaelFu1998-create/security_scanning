def log_in_to_required_registries():
    """Client-side command which runs the user through a login flow
    (via the Docker command-line client so auth is persisted)
    for any registries of active images which require a login. This
    is based on the `image_requires_login` key in the individual specs."""
    registries = set()
    specs = spec_assembler.get_assembled_specs()
    for spec in specs.get_apps_and_services():
        if 'image' in spec and spec.get('image_requires_login'):
            registries.add(registry_from_image(spec['image']))
    unauthed_registries = registries.difference(get_authed_registries())
    for registry in unauthed_registries:
        log_in_to_registry(registry)