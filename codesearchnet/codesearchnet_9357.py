def _parse_local_mount_uri(self, raw_uri):
    """Return a valid docker_path for a local file path."""
    raw_uri = directory_fmt(raw_uri)
    _, docker_path = _local_uri_rewriter(raw_uri)
    local_path = docker_path[len('file'):]
    docker_uri = os.path.join(self._relative_path, docker_path)
    return local_path, docker_uri