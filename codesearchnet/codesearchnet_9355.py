def make_param(self, name, raw_uri, recursive):
    """Return a *FileParam given an input uri."""
    if not raw_uri:
      return self.param_class(name, None, None, None, recursive, None)
    docker_path, uri_parts, provider = self.parse_uri(raw_uri, recursive)
    return self.param_class(name, raw_uri, docker_path, uri_parts, recursive,
                            provider)