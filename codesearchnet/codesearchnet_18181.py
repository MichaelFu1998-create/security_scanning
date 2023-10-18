def _get_networking_mode(app):
    """
    Get the Marathon networking mode for the app.
    """
    # Marathon 1.5+: there is a `networks` field
    networks = app.get('networks')
    if networks:
        # Modes cannot be mixed, so assigning the last mode is fine
        return networks[-1].get('mode', 'container')

    # Older Marathon: determine equivalent network mode
    container = app.get('container')
    if container is not None and 'docker' in container:
        docker_network = container['docker'].get('network')
        if docker_network == 'USER':
            return 'container'
        elif docker_network == 'BRIDGE':
            return 'container/bridge'

    return 'container' if _is_legacy_ip_per_task(app) else 'host'