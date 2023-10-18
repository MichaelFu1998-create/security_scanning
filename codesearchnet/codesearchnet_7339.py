def copy_to_local(local_path, remote_name, remote_path, demote=True):
    """Copy a path from inside a Dusty container to a path on the
    local filesystem. The path on the local filesystem must be
    wrist-accessible by the user specified in mac_username."""
    if not container_path_exists(remote_name, remote_path):
        raise RuntimeError('ERROR: Path {} does not exist inside container {}.'.format(remote_path, remote_name))
    temp_identifier = str(uuid.uuid1())
    copy_path_inside_container(remote_name, remote_path, os.path.join(constants.CONTAINER_CP_DIR, temp_identifier))
    vm_path = os.path.join(vm_cp_path(remote_name), temp_identifier)
    is_dir = vm_path_is_directory(vm_path)
    sync_local_path_from_vm(local_path, vm_path, demote=demote, is_dir=is_dir)