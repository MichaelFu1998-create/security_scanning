def satisfyVersionFromSearchPaths(name, version_required, search_paths, update=False, type='module', inherit_shrinkwrap=None):
    ''' returns a Component/Target for the specified version, if found in the
        list of search paths. If `update' is True, then also check for newer
        versions of the found component, and update it in-place (unless it was
        installed via a symlink).
    '''
    # Pack, , base class for targets and components, internal
    from yotta.lib import pack

    v = None
    try:
        sv = sourceparse.parseSourceURL(version_required)
    except ValueError as e:
        logging.error(e)
        return None

    try:
        local_version = searchPathsFor(
            name,
            sv.semanticSpec(),
            search_paths,
            type,
            inherit_shrinkwrap = inherit_shrinkwrap
        )
    except pack.InvalidDescription as e:
        logger.error(e)
        return None

    logger.debug("%s %s locally" % (('found', 'not found')[not local_version], name))
    if local_version:
        if update and not local_version.installedLinked():
            #logger.debug('attempt to check latest version of %s @%s...' % (name, version_required))
            v = latestSuitableVersion(name, version_required, registry=_registryNamespaceForType(type))
            if local_version:
                local_version.setLatestAvailable(v)

        # if we don't need to update, then we're done
        if local_version.installedLinked() or not local_version.outdated():
            logger.debug("satisfy component from directory: %s" % local_version.path)
            # if a component exists (has a valid description file), and either is
            # not outdated, or we are not updating
            if name != local_version.getName():
                raise Exception('Component %s found in incorrectly named directory %s (%s)' % (
                    local_version.getName(), name, local_version.path
                ))
            return local_version

        # otherwise, we need to update the installed component
        logger.info('update outdated: %s@%s -> %s' % (
            name,
            local_version.getVersion(),
            v
        ))
        # must rm the old component before continuing
        fsutils.rmRf(local_version.path)
        return _satisfyVersionByInstallingVersion(
            name, version_required, local_version.path, v, type=type, inherit_shrinkwrap=inherit_shrinkwrap
        )
    return None