def create_client() -> APIClient:
    """
    Clients a Docker client.

    Will raise a `ConnectionError` if the Docker daemon is not accessible.
    :return: the Docker client
    """
    global _client
    client = _client()
    if client is None:
        # First try looking at the environment variables for specification of the daemon's location
        docker_environment = kwargs_from_env(assert_hostname=False)
        if "base_url" in docker_environment:
            client = _create_client(docker_environment.get("base_url"), docker_environment.get("tls"))
            if client is None:
                raise ConnectionError(
                    "Could not connect to the Docker daemon specified by the `DOCKER_X` environment variables: %s"
                    % docker_environment)
            else:
                logging.info("Connected to Docker daemon specified by the environment variables")
        else:
            # Let's see if the Docker daemon is accessible via the UNIX socket
            client = _create_client("unix://var/run/docker.sock")
            if client is not None:
                logging.info("Connected to Docker daemon running on UNIX socket")
            else:
                raise ConnectionError(
                    "Cannot connect to Docker - is the Docker daemon running? `$DOCKER_HOST` should be set or the "
                    "daemon should be accessible via the standard UNIX socket.")
        _client = weakref.ref(client)
    assert isinstance(client, APIClient)
    return client