def _create_client(base_url: str, tls: TLSConfig=False) -> Optional[APIClient]:
    """
    Creates a Docker client with the given details.
    :param base_url: the base URL of the Docker daemon
    :param tls: the Docker daemon's TLS config (if any)
    :return: the created client else None if unable to connect the client to the daemon
    """
    try:
        client = APIClient(base_url=base_url, tls=tls, version="auto")
        return client if client.ping() else None
    except:
        return None