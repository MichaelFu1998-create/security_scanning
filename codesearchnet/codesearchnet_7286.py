def remove_exited_dusty_containers():
    """Removed all dusty containers with 'Exited' in their status"""
    client = get_docker_client()
    exited_containers = get_exited_dusty_containers()
    removed_containers = []
    for container in exited_containers:
        log_to_client("Removing container {}".format(container['Names'][0]))
        try:
            client.remove_container(container['Id'], v=True)
            removed_containers.append(container)
        except Exception as e:
            log_to_client(e.message or str(e))
    return removed_containers