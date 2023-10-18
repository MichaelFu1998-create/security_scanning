def execute_from_command_line(argv=None):
    """
    Currently the only entrypoint (manage.py, demosys-admin)
    """
    if not argv:
        argv = sys.argv

    # prog_name = argv[0]
    system_commands = find_commands(system_command_dir())
    project_commands = find_commands(project_command_dir())

    project_package = project_package_name()

    command = argv[1] if len(argv) > 1 else None

    # Are we running a core command?
    if command in system_commands:
        cmd = load_command_class('demosys', command)
        cmd.run_from_argv(argv)
    elif command in project_commands:
        cmd = load_command_class(project_package, command)
        cmd.run_from_argv(argv)
    else:
        print("Available commands:")
        for name in system_commands:
            print(" - {}".format(name))
        for name in project_commands:
            print(" - {}".format(name))