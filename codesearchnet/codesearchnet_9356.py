def _parse_image_uri(self, raw_uri):
    """Return a valid docker_path from a Google Persistent Disk url."""
    # The string replace is so we don't have colons and double slashes in the
    # mount path. The idea is the resulting mount path would look like:
    # /mnt/data/mount/http/www.googleapis.com/compute/v1/projects/...
    docker_uri = os.path.join(self._relative_path,
                              raw_uri.replace('https://', 'https/', 1))
    return docker_uri