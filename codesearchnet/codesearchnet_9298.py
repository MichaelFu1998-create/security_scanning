def _get_prepare_env(self, script, job_descriptor, inputs, outputs, mounts):
    """Return a dict with variables for the 'prepare' action."""

    # Add the _SCRIPT_REPR with the repr(script) contents
    # Add the _META_YAML_REPR with the repr(meta) contents

    # Add variables for directories that need to be created, for example:
    # DIR_COUNT: 2
    # DIR_0: /mnt/data/input/gs/bucket/path1/
    # DIR_1: /mnt/data/output/gs/bucket/path2

    # List the directories in sorted order so that they are created in that
    # order. This is primarily to ensure that permissions are set as we create
    # each directory.
    # For example:
    #   mkdir -m 777 -p /root/first/second
    #   mkdir -m 777 -p /root/first
    # *may* not actually set 777 on /root/first

    docker_paths = sorted([
        var.docker_path if var.recursive else os.path.dirname(var.docker_path)
        for var in inputs | outputs | mounts
        if var.value
    ])

    env = {
        _SCRIPT_VARNAME: repr(script.value),
        _META_YAML_VARNAME: repr(job_descriptor.to_yaml()),
        'DIR_COUNT': str(len(docker_paths))
    }

    for idx, path in enumerate(docker_paths):
      env['DIR_{}'.format(idx)] = os.path.join(providers_util.DATA_MOUNT_POINT,
                                               path)

    return env