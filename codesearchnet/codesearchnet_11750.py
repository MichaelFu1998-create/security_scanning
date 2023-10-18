def _install_from_scratch(python_cmd, use_sudo):
    """
    Install setuptools from scratch using installer
    """

    with cd("/tmp"):
        download(EZ_SETUP_URL)

        command = '%(python_cmd)s ez_setup.py' % locals()
        if use_sudo:
            run_as_root(command)
        else:
            run(command)

        run('rm -f ez_setup.py')