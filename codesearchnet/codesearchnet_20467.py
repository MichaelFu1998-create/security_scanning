def install(env, requirements, args, ignore_activated=False,
            install_dev_requirements=False, quiet=False):
    """Install library or project into virtual environment.

    :param env: Use given virtual environment name.
    :param requirements: Use given requirements file for pip.
    :param args: Pass given arguments to pip script.
    :param ignore_activated:
        Do not run pip inside already activated virtual environment. By
        default: False
    :param install_dev_requirements:
        When enabled install prefixed or suffixed dev requirements after
        original installation process completed. By default: False
    :param quiet: Do not output message to terminal. By default: False
    """
    if os.path.isfile(requirements):
        args += ('-r', requirements)
        label = 'project'
    else:
        args += ('-U', '-e', '.')
        label = 'library'

    # Attempt to install development requirements
    if install_dev_requirements:
        dev_requirements = None
        dirname = os.path.dirname(requirements)
        basename, ext = os.path.splitext(os.path.basename(requirements))

        # Possible dev requirements files:
        #
        # * <requirements>-dev.<ext>
        # * dev-<requirements>.<ext>
        # * <requirements>_dev.<ext>
        # * dev_<requirements>.<ext>
        # * <requirements>dev.<ext>
        # * dev<requirements>.<ext>
        #
        # Where <requirements> is basename of given requirements file to use
        # and <ext> is its extension.
        for delimiter in ('-', '_', ''):
            filename = os.path.join(
                dirname, ''.join((basename, delimiter, 'dev', ext))
            )
            if os.path.isfile(filename):
                dev_requirements = filename
                break

            filename = os.path.join(
                dirname, ''.join(('dev', delimiter, basename, ext))
            )
            if os.path.isfile(filename):
                dev_requirements = filename
                break

        # If at least one dev requirements file found, install dev requirements
        if dev_requirements:
            args += ('-r', dev_requirements)

    if not quiet:
        print_message('== Step 2. Install {0} =='.format(label))

    result = not pip_cmd(env,
                         ('install', ) + args,
                         ignore_activated,
                         echo=not quiet)

    if not quiet:
        print_message()

    return result