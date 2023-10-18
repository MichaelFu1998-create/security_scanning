def _satisfyVersionByInstallingVersion(name, version_required, working_directory, version, type='module', inherit_shrinkwrap=None):
    ''' installs and returns a Component/Target for the specified version requirement into
        'working_directory' using the provided remote version object.
        This function is not normally called via `satisfyVersionByInstalling',
        which looks up a suitable remote version object.
    '''
    assert(version)
    logger.info('download %s', version)
    version.unpackInto(working_directory)
    r = _clsForType(type)(working_directory, inherit_shrinkwrap = inherit_shrinkwrap)
    if not r:
        raise Exception(
            'Dependency "%s":"%s" is not a valid %s.' % (name, version_required, type)
        )
    if name != r.getName():
        raise Exception('%s %s (specification %s) has incorrect name %s' % (
            type, name, version_required, r.getName()
        ))
    # error code deliberately ignored here for now, it isn't clear what the
    # behaviour should be (abort? remove the unpacked state then abort?
    # continue?)
    r.runScript('postInstall')
    return r