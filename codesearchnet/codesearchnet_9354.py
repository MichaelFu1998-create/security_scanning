def parse_uri(self, raw_uri, recursive):
    """Return a valid docker_path, uri, and file provider from a flag value."""
    # Assume recursive URIs are directory paths.
    if recursive:
      raw_uri = directory_fmt(raw_uri)
    # Get the file provider, validate the raw URI, and rewrite the path
    # component of the URI for docker and remote.
    file_provider = self.parse_file_provider(raw_uri)
    self._validate_paths_or_fail(raw_uri, recursive)
    uri, docker_uri = self.rewrite_uris(raw_uri, file_provider)
    uri_parts = job_model.UriParts(
        directory_fmt(os.path.dirname(uri)), os.path.basename(uri))
    return docker_uri, uri_parts, file_provider