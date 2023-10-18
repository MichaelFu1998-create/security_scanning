def update_running_containers_from_spec(compose_config, recreate_containers=True):
    """Takes in a Compose spec from the Dusty Compose compiler,
    writes it to the Compose spec folder so Compose can pick it
    up, then does everything needed to make sure the Docker VM is
    up and running containers with the updated config."""
    write_composefile(compose_config, constants.COMPOSEFILE_PATH)
    compose_up(constants.COMPOSEFILE_PATH, 'dusty', recreate_containers=recreate_containers)