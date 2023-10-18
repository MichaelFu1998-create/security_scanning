def copy_between_containers(source_name, source_path, dest_name, dest_path):
    """Copy a file from the source container to an intermediate staging
    area on the local filesystem, then from that staging area to the
    destination container.

    These moves take place without demotion for two reasons:
      1. There should be no permissions vulnerabilities with copying
         between containers because it is assumed the non-privileged
         user has full access to all Dusty containers.
      2. The temp dir created by mkdtemp is owned by the owner of the
         Dusty daemon process, so if we demoted our moves to/from that location
         they would encounter permission errors."""
    if not container_path_exists(source_name, source_path):
        raise RuntimeError('ERROR: Path {} does not exist inside container {}.'.format(source_path, source_name))
    temp_path = os.path.join(tempfile.mkdtemp(), str(uuid.uuid1()))
    with _cleanup_path(temp_path):
        copy_to_local(temp_path, source_name, source_path, demote=False)
        copy_from_local(temp_path, dest_name, dest_path, demote=False)