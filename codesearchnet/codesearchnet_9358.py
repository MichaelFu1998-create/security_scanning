def _parse_gcs_uri(self, raw_uri):
    """Return a valid docker_path for a GCS bucket."""
    # Assume URI is a directory path.
    raw_uri = directory_fmt(raw_uri)
    _, docker_path = _gcs_uri_rewriter(raw_uri)
    docker_uri = os.path.join(self._relative_path, docker_path)
    return docker_uri