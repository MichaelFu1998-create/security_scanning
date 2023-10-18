def pip_install_to_target(path, requirements=None, local_package=None):
    """For a given active virtualenv, gather all installed pip packages then
    copy (re-install) them to the path provided.

    :param str path:
        Path to copy installed pip packages to.
    :param str requirements:
        If set, only the packages in the supplied requirements file are
        installed.
        If not set then installs all packages found via pip freeze.
    :param str local_package:
        The path to a local package with should be included in the deploy as
        well (and/or is not available on PyPi)
    """
    packages = []
    if not requirements:
        print('Gathering pip packages')
        pkgStr = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        packages.extend(pkgStr.decode('utf-8').splitlines())
    else:
        if os.path.exists(requirements):
            print('Gathering requirement packages')
            data = read(requirements)
            packages.extend(data.splitlines())

    if not packages:
        print('No dependency packages installed!')

    if local_package is not None:
        if not isinstance(local_package, (list, tuple)):
            local_package = [local_package]
        for l_package in local_package:
            packages.append(l_package)
    _install_packages(path, packages)