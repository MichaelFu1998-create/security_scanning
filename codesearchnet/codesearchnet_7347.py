def _compile_docker_commands(app_name, assembled_specs, port_spec):
    """ This is used to compile the command that will be run when the docker container starts
    up. This command has to install any libs that the app uses, run the `always` command, and
    run the `once` command if the container is being launched for the first time """
    app_spec = assembled_specs['apps'][app_name]
    commands = ['set -e']
    commands += _lib_install_commands_for_app(app_name, assembled_specs)
    if app_spec['mount']:
        commands.append("cd {}".format(container_code_path(app_spec)))
        commands.append("export PATH=$PATH:{}".format(container_code_path(app_spec)))
    commands += _copy_assets_commands_for_app(app_spec, assembled_specs)
    commands += _get_once_commands(app_spec, port_spec)
    commands += _get_always_commands(app_spec)
    return commands