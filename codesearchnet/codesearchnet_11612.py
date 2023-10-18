def satisfyVersionByInstalling(name, version_required, working_directory, type='module', inherit_shrinkwrap=None):
    ''' installs and returns a Component/Target for the specified name+version
        requirement, into a subdirectory of `working_directory'
    '''
    v = latestSuitableVersion(name, version_required, _registryNamespaceForType(type))
    install_into = os.path.join(working_directory, name)
    return _satisfyVersionByInstallingVersion(
        name, version_required, install_into, v, type=type, inherit_shrinkwrap = inherit_shrinkwrap
    )