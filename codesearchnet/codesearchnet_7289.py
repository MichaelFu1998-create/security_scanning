def _compose_restart(services):
    """Well, this is annoying. Compose 1.2 shipped with the
    restart functionality fucking broken, so we can't set a faster
    timeout than 10 seconds (which is way too long) using Compose.
    We are therefore resigned to trying to hack this together
    ourselves. Lame.

    Relevant fix which will make it into the next release:
    https://github.com/docker/compose/pull/1318"""

    def _restart_container(client, container):
        log_to_client('Restarting {}'.format(get_canonical_container_name(container)))
        client.restart(container['Id'], timeout=1)

    assembled_specs = get_assembled_specs()
    if services == []:
        services = [spec.name for spec in assembled_specs.get_apps_and_services()]
    logging.info('Restarting service containers from list: {}'.format(services))
    client = get_docker_client()
    for service in services:
        container = get_container_for_app_or_service(service, include_exited=True)
        if container is None:
            log_to_client('No container found for {}'.format(service))
            continue
        stopped_linked_containers = _check_stopped_linked_containers(container, assembled_specs)
        if stopped_linked_containers:
            log_to_client('No running containers {0}, which are linked to by {1}.  Cannot restart {1}'.format(
                              stopped_linked_containers, service))
        else:
            _restart_container(client, container)