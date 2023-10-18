def copy_from_local(local_path, remote_name, remote_path, demote=True):
    """Copy a path from the local filesystem to a path inside a Dusty
    container. The files on the local filesystem must be accessible
    by the user specified in mac_username."""
    if not os.path.exists(local_path):
        raise RuntimeError('ERROR: Path {} does not exist'.format(local_path))
    temp_identifier = str(uuid.uuid1())
    if os.path.isdir(local_path):
        sync_local_path_to_vm(local_path, os.path.join(vm_cp_path(remote_name), temp_identifier), demote=demote)
        move_dir_inside_container(remote_name, os.path.join(constants.CONTAINER_CP_DIR, temp_identifier), remote_path)
    else:
        sync_local_path_to_vm(local_path, os.path.join(vm_cp_path(remote_name), temp_identifier), demote=demote)
        move_file_inside_container(remote_name, os.path.join(constants.CONTAINER_CP_DIR, temp_identifier), remote_path)