def get_app_volume_mounts(app_name, assembled_specs, test=False):
    """ This returns a list of formatted volume specs for an app. These mounts declared in the apps' spec
    and mounts declared in all lib specs the app depends on"""
    app_spec = assembled_specs['apps'][app_name]
    volumes = [get_command_files_volume_mount(app_name, test=test)]
    volumes.append(get_asset_volume_mount(app_name))
    repo_mount = _get_app_repo_volume_mount(app_spec)
    if repo_mount:
        volumes.append(repo_mount)
    volumes += _get_app_libs_volume_mounts(app_name, assembled_specs)
    return volumes