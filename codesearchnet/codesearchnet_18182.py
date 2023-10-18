def _get_container_port_mappings(app):
    """
    Get the ``portMappings`` field for the app container.
    """
    container = app['container']

    # Marathon 1.5+: container.portMappings field
    port_mappings = container.get('portMappings')

    # Older Marathon: container.docker.portMappings field
    if port_mappings is None and 'docker' in container:
        port_mappings = container['docker'].get('portMappings')

    return port_mappings