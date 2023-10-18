def _get_app_libs_volume_mounts(app_name, assembled_specs):
    """ Returns a list of the formatted volume mounts for all libs that an app uses """
    volumes = []
    for lib_name in assembled_specs['apps'][app_name]['depends']['libs']:
        lib_spec = assembled_specs['libs'][lib_name]
        volumes.append("{}:{}".format(Repo(lib_spec['repo']).vm_path, container_code_path(lib_spec)))
    return volumes