def get_dusty_containers(services, include_exited=False):
    """Get a list of containers associated with the list
    of services. If no services are provided, attempts to
    return all containers associated with Dusty."""
    client = get_docker_client()
    if services:
        containers = [get_container_for_app_or_service(service, include_exited=include_exited) for service in services]
        return [container for container in containers if container]
    else:
        return [container
                for container in client.containers(all=include_exited)
                if any(name.startswith('/dusty') for name in container.get('Names', []))]