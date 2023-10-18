def get_lib_volume_mounts(base_lib_name, assembled_specs):
    """ Returns a list of the formatted volume specs for a lib"""
    volumes = [_get_lib_repo_volume_mount(assembled_specs['libs'][base_lib_name])]
    volumes.append(get_command_files_volume_mount(base_lib_name, test=True))
    for lib_name in assembled_specs['libs'][base_lib_name]['depends']['libs']:
        lib_spec = assembled_specs['libs'][lib_name]
        volumes.append(_get_lib_repo_volume_mount(lib_spec))
    return volumes