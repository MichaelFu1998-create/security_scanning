def install(packages, upgrade=False, use_sudo=False, python_cmd='python'):
    """
    Install Python packages with ``easy_install``.

    Examples::

        import burlap

        # Install a single package
        burlap.python_setuptools.install('package', use_sudo=True)

        # Install a list of packages
        burlap.python_setuptools.install(['pkg1', 'pkg2'], use_sudo=True)

    .. note:: most of the time, you'll want to use
              :py:func:`burlap.python.install()` instead,
              which uses ``pip`` to install packages.

    """
    argv = []
    if upgrade:
        argv.append("-U")
    if isinstance(packages, six.string_types):
        argv.append(packages)
    else:
        argv.extend(packages)
    _easy_install(argv, python_cmd, use_sudo)