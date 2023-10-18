def make_param(self, name, raw_uri, disk_size):
    """Return a MountParam given a GCS bucket, disk image or local path."""
    if raw_uri.startswith('https://www.googleapis.com/compute'):
      # Full Image URI should look something like:
      # https://www.googleapis.com/compute/v1/projects/<project>/global/images/
      # But don't validate further, should the form of a valid image URI
      # change (v1->v2, for example)
      docker_path = self._parse_image_uri(raw_uri)
      return job_model.PersistentDiskMountParam(
          name, raw_uri, docker_path, disk_size, disk_type=None)
    elif raw_uri.startswith('file://'):
      local_path, docker_path = self._parse_local_mount_uri(raw_uri)
      return job_model.LocalMountParam(name, raw_uri, docker_path, local_path)
    elif raw_uri.startswith('gs://'):
      docker_path = self._parse_gcs_uri(raw_uri)
      return job_model.GCSMountParam(name, raw_uri, docker_path)
    else:
      raise ValueError(
          'Mount parameter {} must begin with valid prefix.'.format(raw_uri))