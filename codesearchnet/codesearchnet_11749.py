def install_setuptools(python_cmd='python', use_sudo=True):
    """
    Install the latest version of `setuptools`_.

    ::

        import burlap

        burlap.python_setuptools.install_setuptools()

    """

    setuptools_version = package_version('setuptools', python_cmd)
    distribute_version = package_version('distribute', python_cmd)

    if setuptools_version is None:
        _install_from_scratch(python_cmd, use_sudo)
    else:
        if distribute_version is None:
            _upgrade_from_setuptools(python_cmd, use_sudo)
        else:
            _upgrade_from_distribute(python_cmd, use_sudo)