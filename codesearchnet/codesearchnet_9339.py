def _get_filtered_mounts(mounts, mount_param_type):
  """Helper function to return an appropriate set of mount parameters."""
  return set([mount for mount in mounts if isinstance(mount, mount_param_type)])